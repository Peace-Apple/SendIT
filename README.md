## SENDIT
#### Travis-Badge

#### Coveralls-Badge

#### Codeclimate-Badge


### About
SendIT is a courier service that helps users deliver parcels to different destinations. SendIT
provides courier quotes based on weight categories.

### Features
1. Create a parcel delivery order
2. Get all parcel delivery orders
3. Get a specific parcel delivery order
4. Cancel a parcel delivery order
5. Get all parcel delivery orders made by a specific user

### Links

#### Gh-pages:  
https://peace-apple.github.io/SendIT/

This link takes you where the user interface template is hosted on gh-pages.

#### Heroku:    

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
|`/api/v1/parcels/`                                   |GET   |Gets all parcel delivery orders           |
|`/api/v1/parcels/<int:parcel_id>/`                   |GET   |Gets a specific parcel delivery order     |
|`/api/v1/parcels/`                                   |POST  |Posts a parcel delivery order             |
|`/api/v1/parcels/<int:parcel_id>/cancel/`            |PUT   |Updates the status of a delivery order    |
|`/api/v1/users/<int:user_id>/parcels/`               |GET   |Gets all parcel orders for a specific user|

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







