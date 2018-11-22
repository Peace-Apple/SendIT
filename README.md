## SENDIT
[![Build Status](https://travis-ci.org/Peace-Apple/SendIT.svg?branch=develop)](https://travis-ci.org/Peace-Apple/SendIT)
[![Coverage Status](https://coveralls.io/repos/github/Peace-Apple/SendIT/badge.svg?branch=develop)](https://coveralls.io/github/Peace-Apple/SendIT?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/1c2a090696fb6dbedf32/maintainability)](https://codeclimate.com/github/Peace-Apple/SendIT/maintainability)

### About
SendIT is a courier service that helps users deliver parcels to different destinations. SendIT
provides courier quotes based on weight categories.

### Features
- The user can create user accounts and can sign in to the app.
- The user can change the destination of a parcel delivery order.
- The user can view all parcel delivery orders he/she has created.
- Admin can view all parcel delivery orders in the application.
- Admin can change the status of a parcel delivery order.
- Admin can change the present location of a parcel delivery order

### Links

#### Gh-pages:  
https://peace-apple.github.io/SendIT/

This link takes you where the user interface template is hosted on gh-pages.

#### Heroku:    
https://apple-sendit.herokuapp.com/

This link takes you to the api that is hosted on heroku.

### Getting Started 
The following will get you started
#### Prerequisites
You will need to install the following

```bash
- git : To clone, update and make commits to the repository
- python3: The base language used to develop the api
- pip: A python package used to install project requirements
```
#### Installation
The ft-challenge-one folder houses the user interface. To access the user interface, open the index.html.
The ft-challenge-two folder contains the system backend services.
- To install the requirements, run:
- [Python](https://www.python.org/) A general purpose programming language
- [Pip](https://pypi.org/project/pip/) A tool for installing python packages
- [Virtualenv](https://virtualenv.pypa.io/en/stable/)  A tool to create isolated Python environments

#### Development setup
- Create a virtual environment and activate it
    ```bash
     Create: virtualenv venv
     On windows: source /venv/scripts/activate
     On linux: /venv/bin/activate
     
    ```
- Install dependencies 
    ```bash
    pip3 install -r requirements.txt
    ```
- Run the application
    ```bash
    cd SendIT
    python run.py
    ```
- Thereafter you can access the system api Endpoints:

| End Point                                           | Verb |Use                                       |
| ----------------------------------------------------|------|------------------------------------------|
|`/api/v2/auth/signup/`                               |POST  |User signup                               |
|`/api/v2/auth/login/`                                |POST  |User login                                |
|`/api/v2/parcels/`                                   |POST  |Posts a parcel delivery order             |
|`/api/v2/parcels/               `                    |GET   |Gets all parcel delivery orders|
|`/api/v1/users/<int:user_id>/parcels/`               |GET   |Gets all parcel orders for a specific user|
|`/api/v1/parcels/<int:parcel_id>/`                   |GET   |Gets a specific parcel delivery order     |
|`/api/v1/parcels/<int:parcel_id>/cancel/`            |PUT   |Updates the status of a delivery order    |


#### Testing

- To run the tests, run the following commands

```bash
pytest --cov 
```

#### Built With

* [Flask](http://flask.pocoo.org/docs/1.0/) - The web framework used
* [Python](https://www.python.org/) - Framework language
* HTML
* CSS

## Authors

* **Peace Acio** - *Initial work* - [Peace-Apple](https://github.com/Peace-Apple)

## Acknowledgments

* Andela Software Development Community







