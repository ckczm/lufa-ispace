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
