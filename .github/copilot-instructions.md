# LavanderCats Cattery - AI Coding Guidelines

## Architecture Overview
This is a FastAPI-based cattery website with SQLAlchemy ORM, Jinja2 templating, and custom admin interface. The app serves both API endpoints and HTML pages.

**Key Components:**
- `app/main.py`: FastAPI app setup, routes, middleware, and template rendering
- `app/models/`: SQLAlchemy models (Cat, Article, AdoptionRequest, etc.)
- `app/schemas/`: Pydantic validation schemas for API requests/responses
- `app/api/`: REST API endpoints organized by feature (cats, articles, adoption)
- `app/admin/`: Custom admin interface views (not SQLAdmin)
- `templates/`: Jinja2 HTML templates with Tailwind CSS
- `static/`: CSS, JS, and uploaded images
- `app/pdf_utils.py`: PDF generation for contracts and documents

## Database & Migrations
- **Development**: SQLite (`catfarm.db`)
- **Production**: PostgreSQL via `DATABASE_URL` env var
- **Migrations**: Alembic with descriptive revision names
- **Setup**: Run `alembic upgrade head` after model changes

**Migration Pattern:**
```bash
alembic revision -m "add_feature_description"
# Edit the generated file in alembic/versions/
alembic upgrade head
```

## Image Handling
**Dual Storage Strategy:**
- Primary: Base64 encoded images stored in database (`photo_base64`, `featured_image_base64`)
- Fallback: Filesystem storage in `static/uploads/` subdirectories

**Key Files:**
- `app/photo_utils.py`: Image processing, compression, thumbnail generation
- `app/upload_api.py`: Upload endpoints with base64 conversion

**Upload Flow:**
1. Validate file type/size (max 10MB, JPEG/PNG/GIF/WebP)
2. Process with PIL (auto-rotate EXIF, compress to 1200x1200, create 300x300 thumbnail)
3. Store as base64 in database
4. Save to filesystem for backward compatibility

## Document Management
**PDF Generation:**
- `app/pdf_utils.py`: ReportLab-based PDF creation
- Contract and departure instructions PDFs
- Download endpoints: `/contract/pdf`, `/departure-instructions/pdf`

**Document Storage:**
- Text content in `static/uploads/documents/` (contract_text.txt, departure_text.txt)
- Word docs for editing: `static/uploads/documents/*.docx`
- Web pages: `/documents`, `/contract`, `/departure-instructions`

## API Patterns
**Standard CRUD Structure:**
```python
@router.get("/cats/", response_model=List[CatApiResponse])
@router.post("/cats/")
@router.get("/cats/{cat_id}")
@router.put("/cats/{cat_id}")
@router.delete("/cats/{cat_id}")
```

**Error Handling:**
- Use try/catch blocks with `db.rollback()` on exceptions
- Return HTTPException with descriptive messages
- Handle IntegrityError for unique constraints (e.g., litter_code)

**Database Sessions:**
- Always use `db: Session = Depends(get_db)`
- Commit explicitly after changes
- Rollback on exceptions

## Admin Interface
**Custom Implementation (not SQLAdmin):**
- Cookie-based authentication (`access_token` cookie)
- HTML templates in `templates/` (e.g., `cat_admin.html`)
- Server-side rendering with Jinja2 + Tailwind CSS
- Default login: `admin` / `admin123` (development only)

**Admin Routes:**
- `/admin`: Main dashboard
- `/admin/login`: Authentication
- `/admin/cats`: Cat management
- `/admin/articles`: Article management
- `/admin/adoption-questions`: Question management
- `/admin/adoption-requests`: Request management

## Adoption System
**Components:**
- `app/models/adoption.py`: AdoptionRequest, AdoptionQuestion models
- `app/api/adoption.py`: Adoption API endpoints
- `templates/adoption_form.html`: Public adoption form
- `templates/adoption_*.html`: Admin management pages

**Flow:**
1. Customers fill form at `/adoption-form`
2. Questions loaded from database
3. Submissions stored as AdoptionRequest
4. Admin reviews at `/admin/adoption-requests`

## Frontend Integration
**Template Variables:**
- Pass database objects directly to templates
- Format dates: `cat.date_of_birth.strftime('%B %d, %Y')`
- Handle image URLs: prepend `/static/` if not external

**Static Files:**
- CSS: `static/css/` (custom styles + Tailwind)
- JS: `static/js/` + Alpine.js for interactivity
- Images: `static/images/` and `static/uploads/`

**Key Pages:**
- `/`: Homepage
- `/cats`: Cat listings
- `/our-cats`: Breeding cats showcase
- `/news`: Article listings
- `/article/{id}`: Individual articles
- `/documents`: Document index with print/download options

## Development Workflow
**Local Setup:**
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
alembic upgrade head
# Optional: Add sample data
python add_sample_cats.py
python add_sample_articles.py
python add_sample_adoption_questions.py
python add_sample_adoption_requests.py
uvicorn app.main:app --reload
```

**Testing:**
- Basic integration tests in root directory (`test_api.py`, etc.)
- Use urllib for HTTP testing against localhost:8000
- Run tests: `python test_api.py`

**Sample Data Scripts:**
- `add_sample_cats.py`: Populates cat database
- `add_sample_articles.py`: Creates sample articles
- `add_sample_adoption_questions.py`: Sets up adoption form questions
- `add_sample_adoption_requests.py`: Creates test adoption requests

## Deployment
**Docker + Render:**
- `Dockerfile`: Multi-stage build with health checks
- `render.yaml`: Service configuration with PostgreSQL database
- Environment variables: `DATABASE_URL`, `SECRET_KEY`, `PORT`

**Build Process:**
```bash
alembic upgrade head  # Run migrations
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Key Conventions
- **Models**: Use `photo_base64` fields (not deprecated `photo_url`)
- **Schemas**: Include `Config.from_attributes = True` for ORM compatibility
- **Routes**: Group by feature in `app/api/` submodules
- **Templates**: Use descriptive names, access model attributes directly
- **Error Messages**: Be user-friendly and specific
- **File Paths**: Store relative to `static/` in database, handle URL formatting in views
- **Authentication**: Cookie-based with `access_token` cookie for admin routes
- **Image Processing**: Always use `photo_utils.py` for uploads, never direct PIL manipulation
- **PDF Generation**: Use `pdf_utils.py` with ReportLab for documents

## Common Patterns
**Image URL Formatting:**
```python
if cat.photo_url and not cat.photo_url.startswith(('http://', 'https://')):
    cat.photo_url = f"/static/{cat.photo_url}"
```

**Base64 Image Display:**
```python
if cat.photo_base64 and not cat.photo_base64.startswith('data:'):
    cat.photo_base64 = f"data:image/jpeg;base64,{cat.photo_base64}"
```

**Date Handling:**
```python
from datetime import datetime, timezone
cat.updated_at = datetime.now(timezone.utc)
```

**Database Constraints:**
- `litter_code`: Unique identifier for cats
- Handle `IntegrityError` with specific error messages
- Use transactions for multi-step operations

**Admin Route Protection:**
```python
@app.middleware("http")
async def admin_auth_middleware(request: Request, call_next):
    if request.url.path.startswith("/admin") and not request.url.path.startswith("/admin/login"):
        access_token = request.cookies.get("access_token")
        if not access_token:
            return RedirectResponse(url="/admin/login", status_code=302)
    response = await call_next(request)
    return response
```

**Template Date Formatting:**
```python
cat.date_of_birth_formatted = cat.date_of_birth.strftime('%B %d, %Y')
```
