from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
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
                password_hash=get_password_hash("admin123"),
                email="admin@example.com",
                phone="13800138000",
                role="admin"
            )
            db.add(admin_user)
            db.commit()
            print("[OK] Admin account created: admin / admin123")
        else:
            print("[INFO] Admin account already exists")
    except Exception as e:
        print(f"[ERROR] Failed to init admin: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_default_admin()
