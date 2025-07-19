"""
Alert webhook endpoint for Grafana notifications
"""

import logging
from datetime import datetime

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/webhook")
async def alert_webhook(request: Request):
    """
    Receive alert notifications from Grafana
    """
    try:
        alert_data = await request.json()
        logger.warning(f"🚨 ALERT RECEIVED: {alert_data}")

        # Process different alert types
        for alert in alert_data.get("alerts", []):
            alert_name = alert.get("labels", {}).get("alertname", "Unknown")
            severity = alert.get("labels", {}).get("severity", "unknown")
            status = alert.get("status", "unknown")

            if status == "firing":
                logger.error(f"🚨 FIRING ALERT: {alert_name} (Severity: {severity})")
                description = alert.get("annotations", {}).get(
                    "description", "No description"
                )
                logger.error(f"   Description: {description}")

                # Here you could:
                # - Send to Slack
                # - Send email
                # - Create incident ticket
                # - Trigger auto-scaling
                # - Restart services

            elif status == "resolved":
                logger.info(f"✅ ALERT RESOLVED: {alert_name}")

        return JSONResponse(
            content={"status": "success", "message": "Alert processed"}, status_code=200
        )

    except Exception as e:
        logger.error(f"Error processing alert webhook: {e}")
        raise HTTPException(status_code=500, detail="Error processing alert")


@router.get("/status")
async def alert_status():
    """
    Get current alert status
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "webhook_endpoint": "/api/alerts/webhook",
        "description": "Alert webhook endpoint is ready to receive notifications",
    }
