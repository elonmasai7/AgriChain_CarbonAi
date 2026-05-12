from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_id(self, user_id: str) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()

    def get_by_wallet(self, wallet: str) -> Optional[User]:
        return self.db.query(User).filter(User.wallet_address == wallet).first()

    def find_by_login(self, login: str) -> Optional[User]:
        return self.db.query(User).filter(
            or_(User.username == login, User.email == login)
        ).first()

    def update(self, user_id: str, data: dict) -> Optional[User]:
        self.db.query(User).filter(User.id == user_id).update(data)
        self.db.commit()
        return self.get_by_id(user_id)

    def list_by_role(self, role: str, skip: int = 0, limit: int = 100):
        return self.db.query(User).filter(User.role == role).offset(skip).limit(limit).all()

    def count_by_role(self, role: str) -> int:
        return self.db.query(User).filter(User.role == role).count()
