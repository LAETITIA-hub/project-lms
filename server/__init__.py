from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///moringa_study_hub.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.json.compact = False
    
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Import and register blueprints
    from routes.users import users_bp
    from routes.courses import courses_bp
    from routes.enrollments import enrollments_bp
    from routes.discussions import discussions_bp
    
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(courses_bp, url_prefix='/api/courses')
    app.register_blueprint(enrollments_bp, url_prefix='/api/enrollments')
    app.register_blueprint(discussions_bp, url_prefix='/api/discussions')
    
    @app.route('/')
    def home():
        return {"message": "Welcome to MoringaStudyHub API!"}
    
    return app 