from flask import Flask
from flask import current_app, Blueprint, flash, redirect, render_template, request, url_for, send_from_directory
from .config import Config

def create_app():
    app = Flask(__name__, static_folder='./static', template_folder='./templates')
    app.config.from_object(Config)
    
    from .routers import root
    from .routers import models
    from .routers import custom_model
    
    app.register_blueprint(root.router)
    app.register_blueprint(models.router)
    app.register_blueprint(custom_model.router)
    
    return app