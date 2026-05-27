from fastapi import APIRouter, Depends, UploadFile, File, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import List, Optional
import base64
import json
import time
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.detection import Detection, DetectionItem
from app.ml.detector import YOLODetector

router = APIRouter()
detector = YOLODetector()

class DetectionResult(BaseModel):
    bbox: List[float]
    label: str
    label_en: str
    confidence: float

class DetectionResponse(BaseModel):
    image_id: str
    detections: List[DetectionResult]
    result_image: str
    detection_time: float

@router.post("/image", response_model=DetectionResponse)
async def detect_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    start_time = time.time()

    contents = await file.read()
    result = detector.detect_image(contents)

    detection = Detection(
        user_id=current_user.id,
        type="image",
        source_path=file.filename,
        result_image=result["result_image"]
    )
    db.add(detection)
    db.commit()
    db.refresh(detection)

    for item in result["detections"]:
        detection_item = DetectionItem(
            detection_id=detection.id,
            label=item["label"],
            label_en=item["label_en"],
            confidence=item["confidence"],
            bbox=json.dumps(item["bbox"])
        )
        db.add(detection_item)

    db.commit()

    detection_time = (time.time() - start_time) * 1000

    return DetectionResponse(
        image_id=str(detection.id),
        detections=[DetectionResult(**d) for d in result["detections"]],
        result_image=result["result_image"],
        detection_time=detection_time
    )

@router.post("/video")
async def detect_video(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contents = await file.read()
    result = detector.detect_video(contents)

    detection = Detection(
        user_id=current_user.id,
        type="video",
        source_path=file.filename,
        total_frames=result["total_frames"],
        disease_frames=result["disease_frames"],
        disease_rate=result["disease_rate"]
    )
    db.add(detection)
    db.commit()
    db.refresh(detection)

    for i, item in enumerate(result["top_frames"]):
        detection_item = DetectionItem(
            detection_id=detection.id,
            label=item["label"],
            label_en=item["label_en"],
            confidence=item["confidence"],
            frame_id=item["frame_id"]
        )
        db.add(detection_item)

    db.commit()

    return result

@router.websocket("/ws/camera")
async def camera_detection(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            if "image" in message:
                image_data = base64.b64decode(message["image"].split(",")[1])
                result = detector.detect_image(image_data)

                await websocket.send_json({
                    "detections": result["detections"],
                    "result_image": result["result_image"]
                })
    except WebSocketDisconnect:
        pass
