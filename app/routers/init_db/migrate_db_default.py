import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schema.base import ResponseSchema
from app.sql_app.database import get_db
from app.sql_app.models import Permission, Role, RolePermission, User

router = APIRouter()


@router.post("/")
async def migrate_permission(db: Session = Depends(get_db)):
    try:
        with open('app/routers/init_db/role_default.json', encoding='utf-8') as file:
            data = json.loads(file.read())
        db.bulk_insert_mappings(Permission, data['permissions'])
        db.bulk_insert_mappings(Role, data['roles'])
        db.bulk_insert_mappings(RolePermission, data['role_permission'])
        db.bulk_insert_mappings(User, data['users'])
        db.commit()
    except Exception as error:
        print(error.args)
        return ResponseSchema(code="500", status="Error", message="Internal Server Error")

    return ResponseSchema(code="200", status="OK", message="Migrate success!!!")