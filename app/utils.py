from datetime import datetime, timedelta
from functools import wraps
import inspect
import json
from typing import Any, Union
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi_jwt_auth import AuthJWT
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from pydantic import BaseModel, ValidationError

from app.schema.base import ResponseSchema
from app.sql_app.database import SessionLocal, get_db
from app.sql_app.models import Redis
# from fastapi_jwt_auth import AuthJWT

SECRET_KEY="engwebsecretkey"
REFRESH_SECRET_KEY="engwebrefreshsecretkey"
ALGORITHM = "HS256"

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
    Authorize.jwt_required()
    user_id = Authorize.get_raw_jwt()["user_id"]
    permission_request = request.method.lower() + request.scope['route'].path
    permission_list = db.query(Redis.permissions).filter(Redis.user_id == user_id).first()
    if permission_request not in json.loads(permission_list.permissions):
        return False
    return True


# send mail
conf = ConnectionConfig(
   MAIL_USERNAME="dong642001@gmail.com",
   MAIL_PASSWORD="test",
   MAIL_PORT=587,
   MAIL_SERVER="smtp.gmail.com",
   MAIL_TLS=True,
   MAIL_SSL=False
)

def send_mail(template: str, email: list, subject: str):
    message = MessageSchema(
        recipients=email,
        body=template,
        subtype="html"
        )
 
    fm = FastMail(conf)
    try:
        fm.send_message(message)
        print('Send mail success!!!')
        return True
    except Exception as error:
        error_message = str(error.args)
        print(error_message)
        return False