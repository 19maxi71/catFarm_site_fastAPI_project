# LavanderCats Cattery - FastAPI Application

A professional cattery website built with FastAPI. This guide will help you run it on your computer.

## What You Need First

- Python 3.8 or newer (download from [python.org](https://python.org) if you don't have it)
- Git (to download the project)

## Step 1: Download the Project

Open your terminal and run:

```bash
git clone https://github.com/19maxi71/catFarm_site_fastAPI_project.git
cd catFarm_site_fastAPI_project
```

## Step 2: Set Up Python Environment

Create a virtual environment (this keeps things clean):

```bash
python -m venv venv
```

Activate it:

- On macOS/Linux: `source venv/bin/activate`
- On Windows: `venv\Scripts\activate`

## Step 3: Install Dependencies

Install all needed packages:

```bash
pip install -r requirements.txt
```

## Step 4: Set Up the Database

Initialize the database:

```bash
alembic upgrade head
```

Add some sample cats and articles (optional scripts):

```bash
python add_sample_cats.py
python add_sample_articles.py
```

## Step 5: Run the Website

Start the server:

```bash
uvicorn app.main:app --reload
```

## Step 6: View the Website

Open your web browser and go to: `http://localhost:8000`

You should see the cattery website!

## Admin Panel

To manage content, go to: `http://localhost:8000/admin`

Default login:

- Username: `admin`
- Password: `admin123`

## Troubleshooting

If you get errors:

1. Make sure Python is installed: `python --version`
2. Make sure you're in the virtual environment (see step 2)
3. Try reinstalling dependencies: `pip install -r requirements.txt`
4. If database errors, delete `catfarm.db` and run `alembic upgrade head` again

## Features

- View cats and their photos
- Read articles about the cattery
- Admin panel to add/edit content
- Responsive design (works on phone/tablet)

## Deploying Online (Optional)

If you want to put this online, you can use:

- **Render.com** (free tier available)
- **Heroku**
- **Docker** (see Dockerfile)

For Render, just connect your GitHub repo and it will auto-deploy.

Enjoy your cattery website! 🐾
