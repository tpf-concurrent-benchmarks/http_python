# HTTP Server in Python

## Objective

This is a python implementation of an HTTP polls server.

## Deployment

### Requirements

- [Docker >3](https://www.docker.com/) (needs docker swarm)
- [Python >3.10](https://www.python.org/) (for local development)

### Configuration

The following environment variables must be defined in the `.env` file:

- `SECRET_KEY`: A secret key for encrypting the JWT tokens.
- `ALGORITHM`: The algorithm used for encrypting the JWT tokens.
- `ACCESS_TOKEN_EXPIRE_MINUTES`: The expiration time for the JWT tokens, in minutes.
- `STATSD_HOST`: The host of the statsd server. Artillery will send metrics to this server.
- `STATSD_PORT`: The port of the statsd server.
- `APP_HOST`: The host of the application.
- `APP_PORT`: The port of the application.
- `DATABASE_URL`: The URL of the database to use. Currently, only SQLite is supported.

Example values for every variable can be found in the [.env.example](.env.example) file. If no `.env` file is found, this file will be copied to `.env`.

### Commands

#### Startup

- `make setup`: Sets up everything needed for the application to run in Docker Swarm.

#### Run

- `make deploy`: Builds the necessary Docker images and deploys the application to Docker Swarm, alongside with Graphite, Grafana and cAdvisor.
- `make remove`: Removes all services created by the `deploy` command.

### Monitoring

- Grafana: [http://127.0.0.1:8081](http://127.0.0.1:8081)
- Graphite: [http://127.0.0.1:8080](http://127.0.0.1:8080)

## Used libraries

- [FastAPI](https://fastapi.tiangolo.com/): A modern, web framework for building APIs with Python
- [Uvicorn](https://www.uvicorn.org/): An ASGI web server implementation for Python.
- [python-jose](https://python-jose.readthedocs.io/en/latest/): A JOSE implementation in Python
- [SQLAlchemy](https://www.sqlalchemy.org/): A SQL toolkit and Object-Relational Mapping (ORM) library for Python
- [Pydantic](https://pydantic-docs.helpmanual.io/): Data validation using Python type hints
- [Passlib](https://passlib.readthedocs.io/en/stable/): Secure password hashing