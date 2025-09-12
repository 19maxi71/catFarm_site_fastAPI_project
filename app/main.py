from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqladmin import Admin, ModelView
from .database import Base, engine, get_db
from .models import Cat, Article
from .admin import CatAdmin
from .api.cats import router as cats_router
from .api.articles import router as articles_router


app = FastAPI(title="RocKaRan Cat Farm",
              description="Siberian Cat Breeding Farm")

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
async def cats_page(request: Request, db: Session = Depends(get_db)):
    # Fetch all cats from the database
    cats = db.query(Cat).all()

    # Convert Cat objects to dictionaries for JSON serialization
    cats_data = []
    for cat in cats:
        cat_dict = {
            "id": cat.id,
            "name": cat.name,
            "role": cat.role,
            "breed": cat.breed,
            "bio": cat.bio,
            "photo_url": cat.photo_url,
            "rabies_vaccinated": cat.rabies_vaccinated,
            "award": cat.award,
            "created_at": cat.created_at.isoformat() if cat.created_at else None,
            "updated_at": cat.updated_at.isoformat() if cat.updated_at else None
        }
        cats_data.append(cat_dict)

    return templates.TemplateResponse("cats.html", {
        "request": request,
        "cats": cats_data
    })


@app.get("/news")
async def news_page(request: Request):
    return templates.TemplateResponse("news.html", {"request": request})
