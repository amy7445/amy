from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import desc
from pydantic import BaseModel
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.detection import Detection, DetectionItem
from app.ml.detector import YOLODetector
import json

router = APIRouter()
detector = YOLODetector()

class EvaluationResponse(BaseModel):
    previous_count: int
    current_count: int
    change: float
    evaluation: str

@router.post("/compare")
async def evaluate_effect(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contents = await file.read()
    result = detector.detect_image(contents)

    current_count = len([d for d in result["detections"] if d["label"] != "healthy"])

    last_detection = db.query(Detection).filter(
        Detection.user_id == current_user.id,
        Detection.type == "evaluation"
    ).order_by(desc(Detection.created_at)).first()

    if last_detection:
        items = db.query(DetectionItem).filter(
            DetectionItem.detection_id == last_detection.id
        ).all()
        previous_count = len([item for item in items if item.label != "healthy"])
    else:
        previous_count = current_count

    if previous_count > 0:
        change = ((current_count - previous_count) / previous_count) * 100
    else:
        change = 0 if current_count == 0 else 100

    evaluation = "有效" if change <= -20 else ("一般" if change <= 20 else "无效")

    detection = Detection(
        user_id=current_user.id,
        type="evaluation",
        source_path=file.filename,
        result_image=result["result_image"]
    )
    db.add(detection)
    db.commit()

    return EvaluationResponse(
        previous_count=previous_count,
        current_count=current_count,
        change=round(change, 1),
        evaluation=evaluation
    )
