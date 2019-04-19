"""
app root of the api endpoints. this module runs the application
"""

from flask import Flask
from api.views.routes import Routes
from flask_jwt_extended import JWTManager
from api.models.database import DatabaseConnection
from flasgger import Swagger
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
Swagger(app)
app.env = 'development'
Routes.generate(app)
app.config['JWT_SECRET_KEY'] = 'apple123'
jwt = JWTManager(app)


@app.route('/')
def index():
    return 'Welcome to SendIT, We deliver your parcels as fast as you make your orders!'

data = DatabaseConnection()
if __name__ == '__main__':
    data.check_admin()
    app.run(debug=True)
