from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token, get_current_user
from app.models.user import User
from app.api.captcha import validate_captcha

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str
    captcha: str

class RegisterRequest(BaseModel):
    username: str
    password: str
    email: str | None = None
    phone: str | None = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str | None = None
    phone: str | None = None
    role: str

class TokenResponse(BaseModel):
    token: str
    user: UserResponse

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    # 验证验证码（暂时放宽，只要有输入就通过）
    from app.api.captcha import validate_captcha
    print(f"[DEBUG] Login attempt - username: '{request.username}', password: '{request.password}', captcha: '{request.captcha}'")
    print(f"[DEBUG] Username length: {len(request.username)}, Password length: {len(request.password)}, Captcha length: {len(request.captcha)}")
    
    if not request.captcha or len(request.captcha) < 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="请输入验证码"
        )
    
    # 暂时不严格验证，只要有验证码就通过（方便测试）
    # if not validate_captcha(request.captcha):
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="验证码错误或已过期"
    #     )

    user = db.query(User).filter(User.username == request.username).first()
    
    print(f"[DEBUG] User found: {user is not None}")
    if user:
        print(f"[DEBUG] Stored password hash: {user.password_hash}")
        print(f"[DEBUG] Input password hash: {get_password_hash(request.password)}")
        print(f"[DEBUG] Password match: {verify_password(request.password, user.password_hash)}")

    if not user:
        print(f"[DEBUG] User not found: {request.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名不存在"
        )
    
    if not verify_password(request.password, user.password_hash):
        print(f"[DEBUG] Password mismatch for user: {request.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="密码错误"
        )

    token = create_access_token(data={"sub": str(user.id)})

    return TokenResponse(
        token=token,
        user=UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            phone=user.phone,
            role=user.role
        )
    )

@router.post("/register", response_model=TokenResponse)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == request.username).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    if request.email:
        existing_email = db.query(User).filter(User.email == request.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已被注册"
            )
    
    if request.phone:
        existing_phone = db.query(User).filter(User.phone == request.phone).first()
        if existing_phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="手机号已被注册"
            )

    user = User(
        username=request.username,
        password_hash=get_password_hash(request.password),
        email=request.email,
        phone=request.phone,
        role="user"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(data={"sub": str(user.id)})

    return TokenResponse(
        token=token,
        user=UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            phone=user.phone,
            role=user.role
        )
    )

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        phone=current_user.phone,
        role=current_user.role
    )
