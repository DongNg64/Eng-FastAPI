from fastapi import FastAPI
import uvicorn
from app.routers import auth

app = FastAPI()

# Sử dụng tệp router users
app.include_router(auth.router, prefix="/api/v1")

# if __name__ == '__main__':
#     uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)
