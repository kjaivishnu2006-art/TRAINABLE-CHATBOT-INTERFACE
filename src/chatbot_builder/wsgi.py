"""
Production-ready WSGI entry point for Flask API
Use with gunicorn or other production servers
"""

from app import app, db

# Ensure database is created
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()
