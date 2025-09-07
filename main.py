from flask import Flask
from config.environment import DEBUG, API_HOST, API_PORT, API_TITLE, API_VERSION
from db.init_db import init_database
from api.routes import api

app = Flask(__name__)


@app.route('/')
def index():
    return "Column Operations API - Check /apidocs for API documentation"

if __name__ == '__main__':
    # Initialize database at startup
    init_database()
    app.run(host=API_HOST, port=API_PORT, debug=DEBUG)