#This have core logic lives here (Flask app created here)

from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from flask_cors import CORS
from .config import Config
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


limiter= Limiter(key_func=get_remote_address)
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    limiter.init_app(app)
    app.config.from_object(Config)
    Swagger(app,template_file='docs/swagger.yaml') 

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app,resources={r"/*":{"origins":"*"}}) #This will allow all incoming requests regardless of origin.
    
    #Register the Blueprints(Routes)
    from .routes import main as main_blueprint
    from .auth import auth as auth_blueprint
    from .doctors import doctors_blueprint
    from .recommend import recommend_bp
    from .appointments import appointments_bp
    from .admin import admin_bp
    
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(doctors_blueprint)
    app.register_blueprint(recommend_bp) 
    app.register_blueprint(appointments_bp)    
    app.register_blueprint(admin_bp) 
    
    
    @app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify({
            "error": "Rate limit exceeded. Please wait and try again."
        }), 429

    return app
