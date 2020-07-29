# Lufthansa-iSpace
> **Micro-service web application** created for internal trainings, easy to use, coded in **Python Flask Framework** - Features:

- UI Kit: Bootstrap 4, Font Awesome
- Database: PostgreSQL, SQLAlchemy ORM
- Modular design with **Blueprints**
- Session-based authentication (via **flask_login**)
- Forms validation and CRUD table
- Deployment scripts: docker-compose

> The Lufthansa-iSpace can be used in many different internal trainings, that cover knowledge in the areas of:

- Performance testing (**backend-side** and **frontend-side** via Google Lighthouse)
- Functional testing of the web application in automated fashion (Selenium, Cypress frameworks etc.) in different approaches: BDD, ATDD etc.
- API testing
- Exploratory testing

> Screenshots:

![Login Page](/media/login_page.jpg?raw=true "Login Page")
![Flight List](/media/flight_list.jpg?raw=true "Flight List")
![Solar System Map](/media/map_page.jpg?raw=true "Solar System Map")

<br />

## How to use it

```bash
$ # Requirements:
$ # - installed git
$ # - installed docker and docker-compose
$
$ # 1. Get the app
$ git clone
$ 
$ # 2. Go to project directory
$ cd lufthansa-ispace
$
$ # 3. Launch application via docker-compose
$ docker-compose
$
$ # Activate python virtual environment
$ # Unix based system:
$ . env/bin/activate
$
$ # Windows:
$ .\env\Scripts\activate
$
$ # Install project packages
$ pip install -r requirements.txt --user
$
$ # Run application
$ python run.py


```
<br />

## Code-base structure

The project is coded using blueprints, app factory pattern, dual configuration profile (development and production) and an intuitive structure presented bellow:

```bash
< PROJECT ROOT >
   |
   |-- app/
   |    |-- static/
   |    |    |-- images/                         # Lufthansa logo and background images
   |    |    |-- scripts/                        # Javascript files
   |    |    |    |--flight_list.js              # Validate all flight list operations - create, calculate, delete
   |    |    |    |--map/
   |    |    |        |-- prefixfree.min.js      # Planets movement system
   |    |    |        |-- scripts.js             # Handles different map views
   |    |    |
   |    |    |-- styles/
   |    |         |--map/                        # CSS files for solar system map
   |    |         |--base.css                    # Styles for navigation bar
   |    |         |--index.css                   # Styles for flight list page
   |    |         |--login.css                   # Styles for login/sign-up pages
   |    |
   |    |-- templates/
   |    |    |--base.html                        # Base html template
   |    |    |--index.html                       # Flight List page
   |    |    |--login.html                       # Login page
   |    |    |--map.html                         # Solar system map page
   |    |    |--singup.html                      # Sign-up page
   |    |
   |    |-- __init__.py                          # Initialize the app
   |    |-- auth.py                              # Auth Blueprint - handles the authentication
   |    |-- main.py                              # Main Blueprint - core backend functionalities for flight list
   |    |-- models.py                            # Database models - SQLAlchemy
   |
   |-- media/                                    # Store app screenshots for readme file
   |-- requirements.txt                          # Python required packages
   |-- .env                                      # Inject Configuration via Environment
   |-- run.py                                    # Start the app - WSGI gateway
   |
   |-- ************************************************************************
```

<br />
