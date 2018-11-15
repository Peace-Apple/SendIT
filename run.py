"""
app root of the api endpoints. this module runs the application
"""

from flask import Flask
from api.views.routes import Routes

app = Flask(__name__)
app.env = 'development'
Routes.generate(app)


@app.route('/')
def index():
    return 'Welcome to SendIT, We deliver your parcels as fast as you make your orders!'


if __name__ == '__main__':
    app.run()

