from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.core.database import Base

class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(String(20), nullable=False)  # image, video, camera
    source_path = Column(String(500))
    total_frames = Column(Integer)
    disease_frames = Column(Integer)
    disease_rate = Column(Float)
    result_image = Column(Text)  # Base64 encoded result image
    created_at = Column(DateTime, server_default=func.now())

class DetectionItem(Base):
    __tablename__ = "detection_items"

    id = Column(Integer, primary_key=True, index=True)
    detection_id = Column(Integer, ForeignKey("detections.id"), nullable=False)
    label = Column(String(100))
    label_en = Column(String(100))
    confidence = Column(Float)
    bbox = Column(Text)  # JSON string
    frame_id = Column(Integer)

class History(Base):
    __tablename__ = "histories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(String(50), nullable=False)  # detection, treatment, evaluation
    data = Column(Text)  # JSON string
    created_at = Column(DateTime, server_default=func.now())
