from datetime import datetime, timedelta
from functools import wraps
import inspect
from typing import Any, Union
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi_jwt_auth import AuthJWT
from jose import jwt
from pydantic import BaseModel, ValidationError

from app.schema.base import ResponseSchema
from app.sql_app.database import SessionLocal, get_db
from app.sql_app.models import Redis
# from fastapi_jwt_auth import AuthJWT

SECRET_KEY="engwebsecretkey"
REFRESH_SECRET_KEY="engwebrefreshsecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)


# create access token
def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt

# create refresh token
def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"

# callback to get your configuration
@AuthJWT.load_config
def get_config():
    return Settings()

# exception handler for authjwt
# # in production, you can tweak performance using orjson response
# @app.exception_handler(AuthJWTException)
# def authjwt_exception_handler(request: Request, exc: AuthJWTException):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"detail": exc.message}
#     )


# def authorization_require():
#     def wrapper(fn):
#         @wraps(fn)
#         def decorator(*args, **kwargs):
#             permission_route = "{0}@{1}".format(requests.method.lower(), request.url_rule.rule)
#             # check permission from redis
#             list_permission = pickle.loads(red.get(f"permission_{get_jwt_identity()}"))
#             if permission_route in list_permission:
#                 return fn(*args, **kwargs)
#             else:
#                 return ResponseSchema(code="500", status="Error", message="You do not have permission")
#         return decorator
#     return wrapper


def auth_required(request: Request, db: SessionLocal = Depends(get_db), Authorize: AuthJWT = Depends()):
    # @wraps(func)
    # async def wrapper(*args, **kwargs):
    # frame = inspect.currentframe().f_back
    # url = frame.f_globals["request"].url
    Authorize.jwt_required()
    user_id = Authorize.get_raw_jwt()["user_id"]
    permission = request.method.lower() + request.scope['route'].path
    db.query(Redis).filter(Redis.user_id == user_id).first()

    if True:
        raise HTTPException(status_code=401, detail="Invalid token")
    else:
        return request.url
    return ResponseSchema(code="500", status="Error", message=request.url)
        # return await func(*args, **kwargs)

    # return wrapper