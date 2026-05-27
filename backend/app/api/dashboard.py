from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.detection import Detection, DetectionItem

router = APIRouter()

DISEASE_LABELS = {
    "healthy": "健康",
    "leaf_spot": "叶斑病",
    "rust": "锈病",
    "powdery_mildew": "白粉病",
    "early_blight": "早疫病",
    "late_blight": "晚疫病"
}

@router.get("/stats")
async def get_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = datetime.now().date()
    today_start = datetime.combine(today, datetime.min.time())

    today_count = db.query(Detection).filter(
        Detection.user_id == current_user.id,
        Detection.created_at >= today_start
    ).count()

    total_detections = db.query(Detection).filter(
        Detection.user_id == current_user.id
    ).all()

    disease_count = 0
    for d in total_detections:
        items = db.query(DetectionItem).filter(DetectionItem.detection_id == d.id).all()
        if any(item.label != "healthy" for item in items):
            disease_count += 1

    disease_rate = disease_count / len(total_detections) if total_detections else 0

    all_items = db.query(DetectionItem).join(Detection).filter(
        Detection.user_id == current_user.id,
        DetectionItem.label != "healthy"
    ).all()

    label_counts = {}
    for item in all_items:
        label_counts[item.label] = label_counts.get(item.label, 0) + 1

    top_disease = "无"
    if label_counts:
        top_label = max(label_counts, key=label_counts.get)
        top_disease = DISEASE_LABELS.get(top_label, top_label)

    return {
        "todayDetectCount": today_count,
        "diseaseRate": disease_rate,
        "topDisease": top_disease,
        "modelStatus": "正常"
    }

@router.get("/trend")
async def get_trend(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = datetime.now().date()
    dates = []
    values = []

    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        day_start = datetime.combine(date, datetime.min.time())
        day_end = datetime.combine(date, datetime.max.time())

        count = db.query(Detection).filter(
            Detection.user_id == current_user.id,
            Detection.created_at >= day_start,
            Detection.created_at <= day_end
        ).count()

        dates.append(date.strftime("%m-%d"))
        values.append(count)

    return {"dates": dates, "values": values}
