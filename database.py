from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# SQLAlchemy
db = SQLAlchemy()

# Migrations
migrate = Migrate()

# Initialise la base de données avec l'application Flask
def init_db(app):
    """Initialise la base de données avec l'application Flask"""
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()  