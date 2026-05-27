from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.ml.llm import TreatmentGenerator

router = APIRouter()
treatment_generator = TreatmentGenerator()

class TreatmentRequest(BaseModel):
    disease_name: str
    severity: str  # light, medium, severe
    crop_type: str

class Pesticide(BaseModel):
    name: str
    concentration: str
    method: str

class Recommendations(BaseModel):
    pesticides: List[Pesticide]
    farming_tips: List[str]
    safety_interval: str

class TreatmentResponse(BaseModel):
    disease: str
    severity: str
    recommendations: Recommendations

DISEASE_NAMES_CN = {
    "leaf_spot": "叶斑病",
    "rust": "锈病",
    "powdery_mildew": "白粉病",
    "early_blight": "早疫病",
    "late_blight": "晚疫病",
    "bacterial_spot": "细菌性斑点病"
}

@router.post("/generate", response_model=TreatmentResponse)
async def generate_treatment(
    request: TreatmentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    disease_cn = DISEASE_NAMES_CN.get(request.disease_name, request.disease_name)

    result = treatment_generator.generate(
        disease=disease_cn,
        severity=request.severity,
        crop_type=request.crop_type
    )

    return TreatmentResponse(
        disease=disease_cn,
        severity=request.severity,
        recommendations=Recommendations(**result)
    )
