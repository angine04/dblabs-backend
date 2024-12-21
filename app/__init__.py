from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from .config import Config
from flask_cors import CORS

db = SQLAlchemy()
ma = Marshmallow()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Handle OPTIONS requests
    @app.route('/api/<path:path>', methods=['OPTIONS'])
    def handle_options(path):
        response = app.make_default_options_response()
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, PATCH'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response
    
    # Add CORS headers after each request
    @app.after_request
    def after_request(response):
        origin = request.headers.get('Origin')
        if origin == 'http://localhost:5173':
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, PATCH'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response
    
    db.init_app(app)
    ma.init_app(app)

    # Register blueprints
    from .routes.course_routes import course_bp
    from .routes.grade_routes import grades_bp
    from .routes.student_routes import student_bp

    app.register_blueprint(course_bp)
    app.register_blueprint(grades_bp)
    app.register_blueprint(student_bp)

    return app