from typing import List

from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT

from app.repository import RoleRepo, UserRepo
from app.schema.base import ResponseSchema, Pagination
from app.schema.user import UsersSchema, UserSchema, UserValidate
from app.sql_app.database import get_db
from sqlalchemy.orm import Session
from app.sql_app.models import Role, User

from app.utils import auth_required, paginate

router = APIRouter()


@router.get("/menutab")
def get_menutab(check_permission: bool = Depends(auth_required), Authorize: AuthJWT = Depends(),
                db: Session = Depends(get_db)):
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


@router.get("", response_model=UsersSchema)
async def get_users(search: str = None,
                    page: int = 1, page_size: int = 10,
                    db: Session = Depends(get_db),
                    check_permission: bool = Depends(auth_required)):
    try:
        if check_permission is False:
            return ResponseSchema(code="400", status="Error", message="You do not permission")
        query = db.query(User)
        if search and len(search) > 0:
            text_like = "%{}%".format(search)
            query = query.filter(User.full_name.ilike(text_like))
        items, page, page_size, total = paginate(query, page, page_size)
        response = UsersSchema(
            code="200",
            status="success",
            message="Get all",
            result=items,
            pagination=Pagination(total=total, page=page, page_size=page_size)
        )
        return response
    except Exception as error:
        print(error.args)
        return ResponseSchema(code="500", status="Error", message="Internal Server Error")


@router.put("/{user_id}")
async def update_user(user_id: str, request_body: UserValidate, db: Session = Depends(get_db),
                      check_permission: bool = Depends(auth_required)):
    try:
        if check_permission is False:
            return ResponseSchema(code="400", status="Error", message="You do not permission")

        user = UserRepo.retrieve_by_id(db, User, user_id)
        if user is None:
            return ResponseSchema(code="400", status="Error", message="Something wrong")
        user.full_name = request_body.dict()['full_name']
        UserRepo.update(db, user)
        return ResponseSchema(code="200", status="Success", message="Update success")
    except Exception as error:
        print(error.args)
        return ResponseSchema(code="500", status="Error", message="Internal Server Error")

