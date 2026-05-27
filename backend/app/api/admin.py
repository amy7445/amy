from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from app.core.database import get_db
from app.core.security import get_current_admin_user
from app.models.user import User
from app.models.detection import Detection, DetectionItem

router = APIRouter()

@router.get("/users")
async def get_users(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    offset = (page - 1) * limit

    total = db.query(User).count()
    users = db.query(User).offset(offset).limit(limit).all()

    return {
        "items": [
            {
                "id": u.id,
                "username": u.username,
                "role": u.role,
                "created_at": u.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
            for u in users
        ],
        "total": total
    }

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return {"error": "用户不存在"}

    if user.role == "admin":
        return {"error": "无法删除管理员用户"}

    db.delete(user)
    db.commit()

    return {"message": "删除成功"}

@router.get("/logs")
async def get_logs(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    logs = [
        {"id": 1, "timestamp": "2024-01-15 10:30:00", "level": "INFO", "message": "用户 admin 登录系统"},
        {"id": 2, "timestamp": "2024-01-15 10:35:00", "level": "INFO", "message": "图片检测完成，检测到2个目标"},
        {"id": 3, "timestamp": "2024-01-15 11:00:00", "level": "WARNING", "message": "模型推理耗时较长"},
        {"id": 4, "timestamp": "2024-01-15 11:30:00", "level": "ERROR", "message": "视频处理失败，文件格式错误"},
    ]

    offset = (page - 1) * limit
    paginated_logs = logs[offset:offset + limit]

    return {
        "items": paginated_logs
    }

@router.put("/profile/password")
async def update_password(
    old_password: str,
    new_password: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    from app.core.security import verify_password, get_password_hash

    if not verify_password(old_password, current_user.password_hash):
        return {"error": "原密码错误"}

    current_user.password_hash = get_password_hash(new_password)
    db.commit()

    return {"message": "密码修改成功"}
