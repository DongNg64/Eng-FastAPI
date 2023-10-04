from fastapi import FastAPI
import uvicorn

from app.routers import auth
from app.routers.init_db import migrate_db_default
from app.routers.manage import user

app = FastAPI()


app.include_router(auth.router, prefix="/auth")
app.include_router(migrate_db_default.router, prefix="/migrate-permission")

# manage
app.include_router(user.router, prefix="/manage/user")

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
