import uuid
from fastapi import APIRouter, Depends, Request
from app.schema.base import RequestSchema, ResponseSchema
from app.schema.auth import LoginRequest, SignupRequest
from sqlalchemy.orm import Session
from app.sql_app.database import get_db
from passlib.context import CryptContext
from app.repository import UserRepo
from app.sql_app.models import User
from datetime import datetime
from fastapi_jwt_auth import AuthJWT

from app.utils import SECRET_KEY, REFRESH_SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, auth_required

router = APIRouter()

# encrypt password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


"""
    Authentication Router

"""


@router.post('/signup')
async def signup(request: SignupRequest, db: Session = Depends(get_db)):
    try:
        exist_email = UserRepo.find_by_email(db, User, request.email)
        if exist_email is not None:
            return ResponseSchema(code="400", status="Error", message="Email is exist")
        _user = User(id=str(uuid.uuid4()),
                      full_name=request.full_name,
                      email=request.email,
                      avatar_url=request.avatar_url,
                      hashed_password=pwd_context.hash(request.password),
                      created_date=datetime.now())
        UserRepo.insert(db, _user)
        return ResponseSchema(code="200", status="Ok", message="Success save data")
    except Exception as error:
        print(error.args)
        return ResponseSchema(code="500", status="Error", message="Internal Server Error")


@router.post('/login')
async def login(request: LoginRequest, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    try:
        email = request.email
        password = request.password
        _user = db.query(User).filter(User.email == email).first()

        if _user is None or not pwd_context.verify(password, _user.hashed_password):
            return ResponseSchema(code="400", status="Bad Request", message="Invalid password")

        another_claims = {"user_id": _user.id}
        access_token = Authorize.create_access_token(subject=_user.email, algorithm=ALGORITHM, expires_time=ACCESS_TOKEN_EXPIRE_MINUTES, user_claims=another_claims)
        refresh_token = Authorize.create_refresh_token(_user.email, algorithm=ALGORITHM, expires_time=REFRESH_TOKEN_EXPIRE_MINUTES)
        token = {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        return ResponseSchema(code="200", status="OK", message="success login!", result=token)
    except Exception as error:
        error_message = str(error.args)
        print(error_message)
        return ResponseSchema(code="500", status="Internal Server Error", message="Internal Server Error")
    

@router.post('/refresh')
async def refresh(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
        email = Authorize.get_jwt_subject()
        new_access_token = Authorize.create_access_token(subject=email)
        return ResponseSchema(code="200", status="OK", message="create access token success!", result=new_access_token)
    except Exception as error:
        error_message = str(error.args)
        print(error_message)
        return ResponseSchema(code="500", status="Internal Server Error", message="Internal Server Error")
    

@router.get('/test/{wdk}')
async def test(dependencies=Depends(auth_required)):
    # a = authorization_require()
    # return a
    return 'ok'