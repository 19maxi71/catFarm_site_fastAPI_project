from starlette.responses import RedirectResponse
from starlette.requests import Request
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware
import os
from .database import Base, engine, get_db
from .models import Cat, Article
from .api.cats import router as cats_router
from .api.articles import router as articles_router
from .api.article_images import router as article_images_router
from .api.adoption import router as adoption_router
from .upload_api import router as upload_router
from .auth import authenticate_user


app = FastAPI(title="RocKaRan Cat Farm",
              description="Siberian Cat Breeding Farm")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add session middleware (required for authentication)
app.add_middleware(SessionMiddleware,
                   secret_key=os.getenv("SECRET_KEY", "dev-secret-key-change-in-production"))

# Serve static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Create database tables
Base.metadata.create_all(bind=engine)

# Custom admin interface (replacing SQLAdmin for better UX)
# No SQLAdmin setup needed - using custom interface at /admin

# Include authentication routes
# Removed - using custom authentication for admin interface

# Include API routes
app.include_router(cats_router, prefix="/api", tags=["cats"])
app.include_router(articles_router, prefix="/api", tags=["articles"])
app.include_router(article_images_router, prefix="/api",
                   tags=["article-images"])
app.include_router(adoption_router, prefix="/api", tags=["adoption"])
app.include_router(upload_router, prefix="/api", tags=["uploads"])

# Admin authentication middleware


@app.middleware("http")
async def admin_auth_middleware(request: Request, call_next):
    """Protect admin routes with authentication."""
    if request.url.path.startswith("/admin") and not request.url.path.startswith("/admin/login"):
        # Check for access token in cookies
        access_token = request.cookies.get("access_token")
        if not access_token:
            return RedirectResponse(url="/admin/login", status_code=302)

        # Here you could verify the token if needed
        # For now, just check if token exists

    response = await call_next(request)
    return response

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
        # Fix photo URL for proper static file serving
        photo_url = cat.photo_url
        if photo_url and not photo_url.startswith(('http://', 'https://')):
            photo_url = f"/static/{photo_url}"

        cat_dict = {
            "id": cat.id,
            "name": cat.name,
            "gender": cat.gender,
            "litter_code": cat.litter_code,
            "date_of_birth": cat.date_of_birth.isoformat() if cat.date_of_birth else None,
            "date_of_birth_formatted": cat.date_of_birth.strftime('%B %d, %Y') if cat.date_of_birth else 'Unknown',
            "description": cat.description,
            "is_available": cat.is_available,
            "photo_url": photo_url,
            "photo_base64": cat.photo_base64,
            "created_at": cat.created_at.isoformat() if cat.created_at else None,
            "updated_at": cat.updated_at.isoformat() if cat.updated_at else None
        }
        cats_data.append(cat_dict)

    return templates.TemplateResponse("cats.html", {
        "request": request,
        "cats": cats_data
    })


@app.get("/our-cats")
async def our_cats_page(request: Request):
    """Serve the Our Cats showcase page featuring breeding cats."""
    return templates.TemplateResponse("our_cats.html", {"request": request})


@app.get("/news")
async def news_page(request: Request):
    return templates.TemplateResponse("news.html", {"request": request})


@app.get("/article/{article_id}")
async def article_detail_page(article_id: int, request: Request, db: Session = Depends(get_db)):
    """Serve individual article detail page."""
    article = db.query(Article).filter(
        Article.id == article_id, Article.published == True).first()

    if not article:
        # Return 404 page or redirect to news
        return templates.TemplateResponse("news.html", {"request": request, "error": "Article not found"})

    # Format featured image URL
    if article.featured_image and not article.featured_image.startswith(('http://', 'https://', '/static/')):
        article.featured_image = f"/static/{article.featured_image}"

    # Get article images
    from .models.article import ArticleImage
    images = db.query(ArticleImage).filter(
        ArticleImage.article_id == article_id).order_by(ArticleImage.display_order).all()

    # Format image URLs for template display
    for image in images:
        if image.image_path and not image.image_path.startswith(('http://', 'https://', '/static/')):
            image.image_path = f"/static/{image.image_path}"

    return templates.TemplateResponse("article_detail.html", {
        "request": request,
        "article": article,
        "images": images
    })


@app.get("/admin/login")
async def admin_login_page(request: Request):
    """Serve admin login page."""
    return templates.TemplateResponse("admin_login.html", {"request": request})


@app.post("/admin/login")
async def admin_login(request: Request):
    """Handle admin login form submission."""
    form_data = await request.form()
    username = form_data.get("username")
    password = form_data.get("password")

    # Simple authentication for now (replace with proper auth later)
    if username == "admin" and password == "admin123":
        # Create access token (simple cookie-based auth for now)
        response = RedirectResponse(url="/admin", status_code=302)
        response.set_cookie(
            key="access_token",
            value="authenticated",  # Simple token for now
            httponly=True,
            max_age=3600  # 1 hour
        )
        return response
    else:
        # Login failed - redirect back to login with error
        return templates.TemplateResponse(
            "admin_login.html",
            {"request": request, "error": "Invalid username or password"}
        )


@app.get("/admin/logout")
async def admin_logout(request: Request):
    """Handle admin logout."""
    response = RedirectResponse(url="/admin/login", status_code=302)
    response.delete_cookie("access_token")
    return response


@app.get("/admin")
async def custom_admin(request: Request):
    """Serve custom admin interface for cat management."""
    return templates.TemplateResponse("cat_admin.html", {"request": request})


@app.get("/admin/articles")
async def article_admin(request: Request):
    """Serve custom admin interface for article management."""
    return templates.TemplateResponse("article_admin.html", {"request": request})


@app.get("/admin/adoption-questions")
async def adoption_questions_admin(request: Request):
    """Serve custom admin interface for adoption questions management."""
    return templates.TemplateResponse("adoption_questions_admin.html", {"request": request})


@app.get("/adoption-form")
async def adoption_form(request: Request):
    """Serve adoption request form for customers."""
    return templates.TemplateResponse("adoption_form.html", {"request": request})


@app.get("/adoption-terms")
async def adoption_terms(request: Request):
    """Serve adoption terms and conditions page."""
    return templates.TemplateResponse("adoption_terms.html", {"request": request})


@app.get("/privacy-policy")
async def privacy_policy(request: Request):
    """Serve privacy policy page."""
    return templates.TemplateResponse("privacy_policy.html", {"request": request})


@app.get("/admin/adoption-requests")
async def adoption_requests_admin(request: Request):
    """Serve custom admin interface for adoption requests management."""
    return templates.TemplateResponse("adoption_requests_admin.html", {"request": request})
