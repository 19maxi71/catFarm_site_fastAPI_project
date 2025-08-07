from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqladmin import Admin, ModelView
from .database import Base, engine
from .models import Cat, Article
from .admin import CatAdmin
from .api.cats import router as cats_router
from .api.articles import router as articles_router


app = FastAPI(title="RocKaRan Cat Farm", description="Siberian Cat Breeding Farm")

# Serve static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize admin
admin = Admin(app, engine)
admin.add_view(CatAdmin)

# Include API routes
app.include_router(cats_router, prefix="/api", tags=["cats"])
app.include_router(articles_router, prefix="/api", tags=["articles"])

# Frontend routes
@app.get("/")
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/cats")
async def cats_page(request: Request):
    return templates.TemplateResponse("cats.html", {"request": request})

@app.get("/news")
async def news_page(request: Request):
    return templates.TemplateResponse("news.html", {"request": request})
