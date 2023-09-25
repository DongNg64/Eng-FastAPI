from typing import TypeVar, Generic, Optional
from sqlalchemy.orm import Session

from datetime import datetime, timedelta
from jose import JWTError, jwt

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException

T = TypeVar('T')


class BaseRepo():

    @staticmethod
    def retrieve_all(db: Session, model: Generic[T]):
        return db.query(model).all()

    @staticmethod
    def retrieve_by_id(db: Session, model: Generic[T], id: int):
        return db.query(model).filter(model.id == id).all()

    @staticmethod
    def insert(db: Session, model: Generic[T]):
        db.add(model)
        db.commit()
        db.refresh(model)

    @staticmethod
    def update(db: Session, model: Generic[T]):
        db.commit()
        db.refresh(model)

    @staticmethod
    def delete(db: Session, model: Generic[T]):
        db.delete(model)
        db.commit()

    
