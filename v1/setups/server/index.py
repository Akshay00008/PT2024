from flask import Flask
from flask_cors import CORS
from ...routes.index import routes

def server():

    app = Flask(__name__)

    CORS(app)

    app.register_blueprint(routes, url_prefix="/api/v1")
    
    return app