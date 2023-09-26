from fastapi import FastAPI
import uvicorn
import app.sql_app.models as model

from app.routers import auth
from app.sql_app.database import engine


app = FastAPI()
model.Base.metadata.create_all(bind=engine)


app.include_router(auth.router, prefix="/auth")

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
