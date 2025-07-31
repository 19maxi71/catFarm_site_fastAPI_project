from fastapi import FastAPI
from sqladmin import Admin, ModelView
from .database import Base, engine
from .models import Cat, Article
from .admin import CatAdmin
from .api.cats import router as cats_router
from .api.articles import router as articles_router


app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize admin
admin = Admin(app, engine)
admin.add_view(CatAdmin)

# Include API routes
app.include_router(cats_router, prefix="/api", tags=["cats"])
app.include_router(articles_router, prefix="/api", tags=["articles"])

@app.get("/")
async def root():
    return {"message": "Welcome to Cat Farm"}
