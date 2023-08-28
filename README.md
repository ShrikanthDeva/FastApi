# FastAPI
This is a sample project that was built by following along the YouTube [Tutorial](https://www.youtube.com/watch?v=0sOvCWFmrtA) and with the help of the FastAPI [documentation](https://fastapi.tiangolo.com/tutorial/) .

* This project focuses on building a fully featured API, that includes **authentication**, **CRUD Operation** and **Schema Validation**
* This project extends well past just basic API development. It also covers the tools that surround in building a complete and robust API

## Tools Learned
* **Postman** - Used to test our API during development
* **Alembic** - A database migration tool
* **Pytest** - Automated testing tool used to verify no pre existing functionalities are broken once you make new changes to your code
* **Ubuntu Deployment** - Deploying our app onto an Ubuntu machine hosted on any cloud platform like AWS, GCP, Azure or DigitalOcean
    * **NGINX** - Setting up nginx webserver that acts as a reverse proxy
    * **Firewall Setup**
    * **SSL Certification**
* **Heroku Deployment** - Deploying our app in heroku, a free cloud platform
* **Docker** - Dockerizing our API
* **CI/CD Pipeline using GitHub Actions** - A pipeline that gets triggered when pushing out changes to GitHub, which runs a series of user-defined automates steps to push out changes to our Production Environment

## Tech Stack
* **Python** - We use Python to build our API
* **FastAPI** - A fast Web framework used to build APIs
* **Postgres** - A free relational DBMS
* **SQLAlchemy** - A popular ORM for python


# commands
+ sudo docker-compose -f docker-compose-dev.yml up
+ localhost:8000/docs