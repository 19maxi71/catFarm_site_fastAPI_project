from fastapi import FastAPI
from sqladmin import Admin, ModelView
from .database import Base, engine
from .models import Cat
from .admin import CatAdmin

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize admin
admin = Admin(app, engine)
admin.add_view(CatAdmin)

@app.get("/")
async def root():
    return {"message": "Welcome to Cat Farm"}
