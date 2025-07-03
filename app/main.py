from fastapi import FastAPI
from sqladmin import Admin, ModelView
from .database import engine
from .models import Base

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize admin
admin = Admin(app, engine)

@app.get("/")
async def root():
    return {"message": "Welcome to Cat Farm"}
