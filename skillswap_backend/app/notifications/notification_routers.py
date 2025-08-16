from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import db_dependancy
from .. import models
from ..auth.auth_utils import get_current_user
from . import notification_schemas
from typing import List

router = APIRouter(prefix='/notifications', tags=["Notifications"])

@router.get("/", response_model=List[notification_schemas.NotificationOut])
def list_notification(db:db_dependancy, current_user:dict=Depends(get_current_user)):
    user = db.query(models.Notification).filter(models.User.email==current_user['email']).first()
    if not user:
        raise HTTPException(status_code=404, detail="Cannot access users")
    return db.query(models.Notification).filter_by(user_id=user.id).order_by(models.Notification.created_at.desc()).all()

@router.post("/{notif_id}/read")
def mark_as_read(notif_id:int, db:db_dependancy, current_user:dict=Depends(get_current_user)):
    notif=db.query(models.Notification).filter_by(id=notif_id).first()
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    notif.is_read = True
    db.commit()
    return {"status":"ok"}