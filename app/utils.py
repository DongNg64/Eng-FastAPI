
import json
from fastapi import Depends, HTTPException, Request
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
        subject=subject,
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