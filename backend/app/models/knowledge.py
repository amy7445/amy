from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base

class KnowledgeBase(Base):
    __tablename__ = "knowledge_base"

    id = Column(Integer, primary_key=True, index=True)
    disease_name = Column(String(100))
    disease_name_en = Column(String(100))
    crop_type = Column(String(50))
    symptoms = Column(Text)
    prevention = Column(Text)
    treatment = Column(Text)
    image_path = Column(String(500))

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    username = Column(String(50))
    content = Column(Text)
