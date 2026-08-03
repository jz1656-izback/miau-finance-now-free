"""
🔔 ALERTS API ENDPOINTS
Create, manage, and retrieve alerts
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from app.middleware.auth import get_current_user
from app.services.alerts_service import (
    alerts_service, AlertType, AlertCondition, AlertSeverity, Alert
)
from app.services.notification_service import notification_service

router = APIRouter(tags=["Alerts"])


# ============================================================================
# SCHEMAS
# ============================================================================

class AlertCreateRequest(BaseModel):
    """Create alert request"""
    alert_type: str = Field(..., description="Type of alert")
    ticker: Optional[str] = Field(None, max_length=5)
    portfolio_id: Optional[str] = None
    condition: str = Field(..., description="Trigger condition (above/below/equals/changes_by)")
    threshold: float = Field(..., description="Alert threshold value")
    severity: str = Field("info", description="Alert severity (info/warning/critical)")
    cooldown_minutes: int = Field(0, ge=0, le=1440, description="Cooldown between triggers")


class AlertResponse(BaseModel):
    """Alert response"""
    alert_id: str
    alert_type: str
    ticker: Optional[str] = None
    portfolio_id: Optional[str] = None
    condition: str
    threshold: float
    current_value: float
    severity: str
    enabled: bool
    status: str
    created_at: str
    last_triggered: Optional[str] = None


class AlertHistoryResponse(BaseModel):
    """Alert history item"""
    timestamp: str
    alert_id: str
    alert_type: str
    ticker: Optional[str]
    price: float
    threshold: float


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/alerts", response_model=AlertResponse)
async def create_alert(
    request: AlertCreateRequest,
    user: dict = Depends(get_current_user),
):
    user_id = user["sub"]
    try:
        alert_type = AlertType(request.alert_type)
        condition = AlertCondition(request.condition)
        severity = AlertSeverity(request.severity)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid alert type, condition, or severity: {str(e)}"
        )
    
    # Validate input
    if request.ticker is None and request.portfolio_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either ticker or portfolio_id must be provided"
        )
    
    alert = await alerts_service.create_alert(
        user_id=user_id,
        alert_type=alert_type,
        ticker=request.ticker,
        portfolio_id=request.portfolio_id,
        condition=condition,
        threshold=request.threshold,
        severity=severity,
        cooldown_minutes=request.cooldown_minutes,
    )
    
    return alert.to_dict()


@router.get("/alerts", response_model=List[AlertResponse])
async def get_alerts(user: dict = Depends(get_current_user)):
    user_id = user["sub"]
    alerts = await alerts_service.get_user_alerts(user_id)
    return [a.to_dict() for a in alerts]


@router.put("/alerts/{alert_id}/enable")
async def enable_alert(
    alert_id: str,
    user: dict = Depends(get_current_user),
):
    user_id = user["sub"]
    alert = await alerts_service.get_alert(alert_id)
    if not alert or alert.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    if not await alerts_service.enable_alert(alert_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to enable alert"
        )
    return {"status": "enabled"}


@router.put("/alerts/{alert_id}/disable")
async def disable_alert(
    alert_id: str,
    user: dict = Depends(get_current_user),
):
    user_id = user["sub"]
    alert = await alerts_service.get_alert(alert_id)
    if not alert or alert.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    if not await alerts_service.disable_alert(alert_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to disable alert"
        )
    return {"status": "disabled"}


@router.delete("/alerts/{alert_id}")
async def delete_alert(
    alert_id: str,
    user: dict = Depends(get_current_user),
):
    user_id = user["sub"]
    alert = await alerts_service.get_alert(alert_id)
    if not alert or alert.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    if not await alerts_service.delete_alert(alert_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete alert"
        )
    return {"status": "deleted"}


@router.get("/alerts/history", response_model=List[AlertHistoryResponse])
async def get_alert_history(
    days: int = 7,
    user: dict = Depends(get_current_user),
):
    user_id = user["sub"]
    history = await alerts_service.get_alert_history(user_id=user_id, days=days)
    return history


# ============================================================================
# EXAMPLE ALERTS (For Testing)
# ============================================================================

@router.post("/alerts/examples")
async def create_example_alerts(user: dict = Depends(get_current_user)):
    """
    Create example alerts for testing
    Demonstrates all alert types
    """
    user_id = user["sub"]
    examples = []
    
    # Price above alert
    alert1 = await alerts_service.create_alert(
        user_id=user_id,
        alert_type=AlertType.PRICE_THRESHOLD,
        ticker="AAPL",
        condition=AlertCondition.ABOVE,
        threshold=180.0,
        severity=AlertSeverity.WARNING,
    )
    examples.append(alert1.to_dict())
    
    # Price change alert
    alert2 = await alerts_service.create_alert(
        user_id=user_id,
        alert_type=AlertType.PRICE_CHANGE,
        ticker="MSFT",
        condition=AlertCondition.CHANGES_BY,
        threshold=5.0,  # 5% change
        severity=AlertSeverity.INFO,
        cooldown_minutes=60,
    )
    examples.append(alert2.to_dict())
    
    # Risk alert (example)
    alert3 = await alerts_service.create_alert(
        user_id=user_id,
        alert_type=AlertType.RISK_ALERT,
        portfolio_id="portfolio_1",
        condition=AlertCondition.ABOVE,
        threshold=0.10,  # 10% VaR
        severity=AlertSeverity.CRITICAL,
    )
    examples.append(alert3.to_dict())
    
    return {
        "message": "Example alerts created",
        "alerts": examples
    }


# ============================================================================
# NOTIFICATION ENDPOINTS
# ============================================================================

class NotificationPreferenceRequest(BaseModel):
    channels: List[str] = Field(..., description="List of channels: email, sms, push, in_app, webhook")


class NotificationSendRequest(BaseModel):
    subject: str = Field(..., max_length=200)
    message: str = Field(..., max_length=2000)
    channels: Optional[List[str]] = None


@router.get("/notifications", summary="Get in-app notifications")
async def get_notifications(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    user: dict = Depends(get_current_user),
):
    in_app = notification_service.get_in_app_provider()
    return in_app.get_all(user["sub"], limit=limit, offset=offset)


@router.get("/notifications/unread", summary="Get unread notification count")
async def get_unread_notifications(user: dict = Depends(get_current_user)):
    in_app = notification_service.get_in_app_provider()
    unread = in_app.get_unread(user["sub"])
    return {"unread_count": len(unread), "notifications": unread}


@router.put("/notifications/read", summary="Mark notifications as read")
async def mark_notifications_read(
    index: Optional[int] = Query(None, description="Specific notification index, or all if omitted"),
    user: dict = Depends(get_current_user),
):
    in_app = notification_service.get_in_app_provider()
    success = in_app.mark_read(user["sub"], index)
    return {"success": success}


@router.delete("/notifications", summary="Clear all notifications")
async def clear_notifications(user: dict = Depends(get_current_user)):
    in_app = notification_service.get_in_app_provider()
    count = in_app.clear(user["sub"])
    return {"cleared": count}


@router.put("/notifications/preferences", summary="Set notification channel preferences")
async def set_notification_preferences(
    req: NotificationPreferenceRequest,
    user: dict = Depends(get_current_user),
):
    from app.services.notification_service import NotificationChannel
    valid = {c.value for c in NotificationChannel}
    channels = []
    for ch in req.channels:
        if ch not in valid:
            raise HTTPException(status_code=400, detail=f"Invalid channel: {ch}. Valid: {', '.join(sorted(valid))}")
        channels.append(NotificationChannel(ch))
    notification_service.set_user_preferences(user["sub"], channels)
    return {"user_id": user["sub"], "channels": req.channels}


@router.get("/notifications/preferences", summary="Get notification channel preferences")
async def get_notification_preferences(user: dict = Depends(get_current_user)):
    channels = notification_service.get_user_preferences(user["sub"])
    return {"user_id": user["sub"], "channels": [c.value for c in channels]}


@router.post("/notifications/send", summary="Send a custom notification")
async def send_notification(
    req: NotificationSendRequest,
    user: dict = Depends(get_current_user),
):
    from app.services.notification_service import NotificationChannel
    channels = None
    if req.channels:
        channels = [NotificationChannel(c) for c in req.channels]
    results = await notification_service.send_custom_notification(
        user_id=user["sub"],
        subject=req.subject,
        message=req.message,
        channels=channels,
    )
    return {"delivered": results}


@router.get("/notifications/history", summary="Get notification delivery history")
async def get_notification_history(
    days: int = Query(30, ge=1, le=365),
    user: dict = Depends(get_current_user),
):
    history = notification_service.get_notification_history(
        user_id=user["sub"],
        days=days,
    )
    return {"history": history, "count": len(history)}
