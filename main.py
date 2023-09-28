from fastapi import FastAPI
import uvicorn
import app.sql_app.models as model

from app.routers import auth
from app.sql_app.database import engine
from app.routers.init_db import migrate_db_default

app = FastAPI()
model.Base.metadata.create_all(bind=engine)


app.include_router(auth.router, prefix="/auth")
app.include_router(migrate_db_default.router, prefix="/migrate-permission")

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
