import os
import json
from flask import Flask, jsonify, make_response, render_template, request
from flask_cors import CORS

from api.core import exception_handler, create_response
from api.config import config_
from api.models import db


def create_app(**config_override):
    """Flask Application Factory
    """
    # Instantiate flask app
    app = Flask(__name__, instance_relative_config=True)

    # Set configurations
    env = os.environ.get("FLASK_ENV", "development")
    print(env)
    app.config.from_object(config_[env])

    db.init_app(app)  # Register database
    CORS(app)  # Add CORS headers

    # TODO: Add logger

    # proxy support for Nginx
    from werkzeug.middleware.proxy_fix import ProxyFix

    app.wsgi_app = ProxyFix(app.wsgi_app)

    # Register blueprints for API endpoints
    from api.endpoints import _main, _filter, _patient_history, _patient_images

    app.register_blueprint(_main._main)
    app.register_blueprint(_filter._filter)
    app.register_blueprint(_patient_history._patient_history)
    app.register_blueprint(_patient_images._patient_images)

    # Register error handler
    app.register_error_handler(Exception, exception_handler)

    return app
