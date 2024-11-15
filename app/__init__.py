from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from apscheduler.schedulers.background import BackgroundScheduler

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    db.init_app(app)
    migrate.init_app(app, db)  # Initialize Flask-Migrate

    with app.app_context():
        from .routes import add_routes
        from .tasks import monitor_websites
        add_routes(app)
        db.create_all()

    # Scheduler setup for periodic tasks
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=lambda: monitor_websites(app), trigger="interval", seconds=app.config['INTERVAL'])
    scheduler.start()

    return app