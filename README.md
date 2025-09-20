# CatFarm Site - FastAPI Application

A beautiful cat farm website with article management system built with FastAPI.

## Features
- 🐱 Cat profiles with photos
- 📝 Article management with featured images and galleries
- 🔐 Admin panel for content management
- 📱 Responsive design with Tailwind CSS
- 🖼️ Automatic photo orientation correction
- 🎨 Modern UI with smooth animations

## Quick Deployment to Render

### Option 1: One-Click Deploy (Recommended)
1. Fork this repository to your GitHub account
2. Go to [Render.com](https://render.com) and sign up/login
3. Click "New +" → "Web Service"
4. Connect your GitHub account and select this repository
5. Configure the service:
   - **Name**: `catfarm-site`
   - **Runtime**: `Docker`
   - **Build Command**: `docker build -t catfarm .`
   - **Start Command**: `docker run -p $PORT:8000 catfarm`
6. Add environment variables:
   - `DATABASE_URL`: Will be auto-configured when you add PostgreSQL
   - `SECRET_KEY`: Generate a random string
7. Add a PostgreSQL database:
   - Click "New +" → "PostgreSQL"
   - Name it `catfarm-db`
   - Connect it to your web service
8. Click "Create Web Service"

### Option 2: Manual Setup
1. Create a Render account
2. Create a PostgreSQL database instance
3. Create a web service with Docker runtime
4. Use the provided `render.yaml` for configuration

## Local Development

```bash
# Clone the repository
git clone <your-repo-url>
cd catFarm_site_fastAPI_project

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database (local SQLite for development)
export DATABASE_URL="sqlite:///./catfarm.db"

# Run database migrations
alembic upgrade head

# Add sample data (optional)
python add_sample_cats.py
python add_sample_articles.py

# Start the server
uvicorn app.main:app --reload
```

Visit `http://localhost:8000` to see your site!

## Admin Access
- Go to `/admin/login`
- Username: `admin`
- Password: `admin123`
- Change these credentials in production!

## Project Structure
```
├── app/
│   ├── api/           # API endpoints
│   ├── models/        # Database models
│   ├── schemas/       # Pydantic schemas
│   ├── templates/     # Jinja2 templates
│   └── ...
├── static/            # Static files (CSS, JS, images)
├── alembic/           # Database migrations
└── requirements.txt   # Python dependencies
```

## Technologies Used
- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Image Processing**: Pillow with EXIF orientation correction
- **Deployment**: Docker, Render

## API Endpoints
- `GET /` - Homepage
- `GET /cats` - Cat profiles
- `GET /news` - Article listing
- `GET /article/{id}` - Individual article
- `GET /admin/*` - Admin panel
- `POST /api/*` - API endpoints

Enjoy your cat farm website! 🐾
