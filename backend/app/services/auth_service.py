from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User, UserRole
from app.repositories.user_repo import UserRepository
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.schemas.auth import UserRegister, UserLogin, TokenResponse


class AuthService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def register(self, data: UserRegister) -> User:
        if self.repo.get_by_email(data.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        if self.repo.get_by_username(data.username):
            raise HTTPException(status_code=400, detail="Username already taken")

        user = User(
            email=data.email,
            username=data.username,
            hashed_password=hash_password(data.password),
            full_name=data.full_name,
            role=data.role,
            phone=data.phone,
            country=data.country,
        )
        return self.repo.create(user)

    def login(self, data: UserLogin) -> TokenResponse:
        user = self.repo.find_by_login(data.username)
        if not user or not verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        if not user.is_active:
            raise HTTPException(status_code=401, detail="Account is inactive")

        access_token = create_access_token({"sub": str(user.id), "role": user.role.value})
        refresh_token = create_refresh_token({"sub": str(user.id)})
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    def refresh_token(self, refresh_token: str) -> TokenResponse:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        user = self.repo.get_by_id(payload["sub"])
        if not user or not user.is_active:
            raise HTTPException(status_code=401, detail="User not found")

        access = create_access_token({"sub": str(user.id), "role": user.role.value})
        refresh = create_refresh_token({"sub": str(user.id)})
        return TokenResponse(access_token=access, refresh_token=refresh)

    def get_profile(self, user_id: str) -> User:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def update_profile(self, user_id: str, data: dict) -> User:
        return self.repo.update(user_id, data)

    def get_user_count_by_role(self, role: str) -> int:
        return self.repo.count_by_role(role)
