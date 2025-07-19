import time

from fastapi import Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
)

# Define metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status"],
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
)

REQUEST_IN_PROGRESS = Gauge(
    "http_requests_in_progress",
    "Number of HTTP requests currently in progress",
    ["method", "endpoint"],
)

# Calculator specific metrics
CALCULATION_COUNT = Counter(
    "calculator_operations_total",
    "Total number of calculator operations",
    ["operation", "status"],
)

CALCULATION_LATENCY = Histogram(
    "calculator_operation_duration_seconds",
    "Calculator operation latency in seconds",
    ["operation"],
)


def get_metrics():
    """Generate Prometheus metrics"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


class PrometheusMiddleware:
    """Middleware to collect Prometheus metrics"""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        method = scope["method"]
        path = scope["path"]

        # Track request in progress
        REQUEST_IN_PROGRESS.labels(method=method, endpoint=path).inc()

        start_time = time.time()

        # Create a custom send function to capture response status
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                status = message["status"]
                REQUEST_COUNT.labels(method=method, endpoint=path, status=status).inc()

            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            # Record latency
            duration = time.time() - start_time
            REQUEST_LATENCY.labels(method=method, endpoint=path).observe(duration)

            # Decrease request in progress
            REQUEST_IN_PROGRESS.labels(method=method, endpoint=path).dec()
