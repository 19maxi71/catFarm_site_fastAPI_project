#!/bin/bash
# Database initialization script for deployment

echo "Initializing database..."

# Wait for database to be ready
sleep 10

# Run database migrations
alembic upgrade head

# Run sample data scripts if they exist
if [ -f "add_sample_cats.py" ]; then
    echo "Adding sample cats..."
    python add_sample_cats.py
fi

if [ -f "add_sample_articles.py" ]; then
    echo "Adding sample articles..."
    python add_sample_articles.py
fi

echo "Database initialization complete!"
