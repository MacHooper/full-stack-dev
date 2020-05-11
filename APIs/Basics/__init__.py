from flask import Flask, jsonfiy
from flask_cors import CORS
from models import setup_db, Plant

def create_app(test_config=None):
    app = Flask(__name__)
    setup.db(app)
    CORS(app)

    @app.after_request # Says after a request is received, run this method
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization') # Enables content specification, and authorization.
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS') # Specify methods the app will be using.
        return response

    @app.route('/') 
    def hello():
        return jsonify({'message': 'HELLO WORLD'})

    return app
