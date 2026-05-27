from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.api import auth, detection, dashboard, treatment, evaluation, history, knowledge, admin, captcha
from app.core.database import engine, Base, SessionLocal
from app.core.security import get_password_hash
from app.models.user import User

Base.metadata.create_all(bind=engine)

def init_default_admin():
    db = SessionLocal()
    try:
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            admin_user = User(
                username="admin",
                password_hash=get_password_hash("admin"),
                role="admin"
            )
            db.add(admin_user)
            db.commit()
            print("[OK] Admin account created: admin / admin")
        else:
            # 更新密码为 admin
            admin_user.password_hash = get_password_hash("admin")
            admin_user.role = "admin"
            db.commit()
            print("[OK] Admin account updated: admin / admin")
    except Exception as e:
        print(f"[ERROR] Failed to init admin: {e}")
    finally:
        db.close()

init_default_admin()

app = FastAPI(
    title="智慧农害 - 农作物病虫害检测与防治系统",
    description="基于YOLOv11与LLM的农作物病虫害检测与防治系统API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:5174", "http://127.0.0.1:5174", "http://localhost:5175", "http://127.0.0.1:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(captcha.router, prefix="/api", tags=["验证码"])
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["数据看板"])
app.include_router(detection.router, prefix="/api/detect", tags=["检测"])
app.include_router(treatment.router, prefix="/api/treatment", tags=["防治方案"])
app.include_router(evaluation.router, prefix="/api/evaluation", tags=["效果评估"])
app.include_router(history.router, prefix="/api/history", tags=["历史记录"])
app.include_router(knowledge.router, prefix="/api/knowledge", tags=["知识库"])
app.include_router(admin.router, prefix="/api/admin", tags=["管理员"])

@app.get("/")
async def root():
    return {"message": "智慧农害 API 服务运行中"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
