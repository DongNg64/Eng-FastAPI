from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from app.repository import RoleRepo, UserRepo
from app.schema.base import ResponseSchema
from app.sql_app.database import get_db
from sqlalchemy.orm import Session
from app.sql_app.models import Role, User

from app.utils import auth_required


router = APIRouter()

@router.get("/menutab")
def get_menutab(check_permission: bool = Depends(auth_required), Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    if check_permission is False:
        return ResponseSchema(code="400", status="Error", message="You do not permission")
    
    try:
        user_id = Authorize.get_raw_jwt()["user_id"]
        user = UserRepo.retrieve_by_id(db=db, model=User, id=user_id)
        if user is None:
            return ResponseSchema(code="500", status="Error", message="User not exist")
        
        role = RoleRepo.retrieve_by_id(db=db, model=Role, id=user.role_id)
        return ResponseSchema(code="200", status="OK", message="get menutab success!!!", result=role.key)
    except Exception as error:
        error_message = str(error.args)
        print(error_message)
        return ResponseSchema(code="500", status="Internal Server Error", message="Internal Server Error")
   
    
