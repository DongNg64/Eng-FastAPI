from fastapi import APIRouter, Depends

from app.schema.base import ResponseSchema
from app.sql_app.database import get_db
from app.utils import auth_required
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("", summary="Get all listening")
async def get_all(check_permission: bool = Depends(auth_required), 
                  db: Session = Depends(get_db),
                  page: int = 1, page_size: int = 10, search: str = None,
                  type: int = 1):
    if check_permission is False:
        return ResponseSchema(code="400", status="Error", message="You do not permission")

    try:
        query = db.query(Listening)


    except Exception as error:
        error_message = str(error.args)
        print(error_message)
        return ResponseSchema(code="500", status="Internal Server Error", message="Internal Server Error")