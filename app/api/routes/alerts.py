"""
Alert webhook endpoint for Grafana notifications
"""

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
import logging
from typing import Dict, Any
from datetime import datetime

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
                logger.error(
                    f"   Description: {alert.get('annotations', {}).get('description', 'No description')}"
                )

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
