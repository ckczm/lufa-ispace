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

>Thanks to branches with various intentionally implemented errors, this application offers many different test scenarios that can be used in training by easily switching between prepared branches. To create your own version of the application with a new defined bug, just create your branch based on the master one and implement it.

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
$ git clone https://U552249@bitbucket.dev.lsy.pl/scm/~u552249/lufthansa-ispace.git
$ 
$ # 2. Go to project directory
$ cd lufthansa-ispace
$
$ # 3. Build docker image of the application
$ docker build -t ispace_web_server . (trza wylaczyc firmowego neta)
$
$ # 4. Pull official postgres database image
$ git pull postgres
$
$ # 5. Create docker network
$ docker network create ispace_network
$
$ # 6. Launch application via docker-compose 
$ docker-compose up -d
$
$ # 7. Done! Application is available at http://localhost:5000
$
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
   |-- docker/                                   # Store docker-compose file
   |-- Dockerfile                                # Dockerfile for building ispace app docker image
   |-- media/                                    # Store app screenshots for readme file
   |-- requirements.txt                          # Python required packages
   |-- .env                                      # Inject Configuration via Environment
   |-- run.py                                    # Start the app - WSGI gateway
   |
   |-- ************************************************************************
```

<br />
