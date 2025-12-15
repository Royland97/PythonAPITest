# PythonTestAPI

This project consists of the design and implementation of a REST API developed in Python using the FastAPI framework with MongoDB. The API consumes information from the Spaceflight News API, an external source that provides news and reports related to space flights, missions and space stations published by various web media.

url: https://www.spaceflightnewsapi.net/ 

The objective of the project is to manage, store and expose this data in a structured way through REST endpoints, applying best practices in architecture, modularity, and modern API development.

Requirements
- Python 3.10+
- Docker

For local deployment install dependencies:
<pre>pip install -r requirements.txt</pre>

Running with Docker
<pre>docker-compose up --build -d</pre>

Stop the service
<pre>docker-compose down</pre>

## ▶️ Start API

Once running (with Docker or local), you can access **Swagger UI:**  
https://localhost:443/docs

## Users Endpoints

| Method | Path           | Description            |
|--------|----------------|------------------------|
| GET    | `/users/`      | Get all users          |
| POST   | `/users/`      | Create a new user      |
| GET    | `/users/{id}`  | Get user by ID         |
| PUT    | `/users/{id}`  | Update user by ID      |
| DELETE | `/users/{id}`  | Delete user by ID      |

## Auth Endpoints

| Method | Path           | Description    |
|--------|----------------|----------------|
| POST   | `/auth/login`  | Login          |

## Article Endpoints

| Method | Path                      | Description                                   |
|--------|---------------------------|-----------------------------------------------|
| POST   | `/articles/sync`          | Start synchronization with SpaceflightNewsAPI |
| GET    | `/articles/sync/progress` | Get sync progress                             |
| POST   | `/articles/sync/cancel`   | Cancel synchronization                        |
| GET    | `/articles/`              | Get articles                                  |

## Report Endpoints

| Method | Path                     | Description                                    |
|--------|--------------------------|------------------------------------------------|
| POST   | `/reports/sync`          | Start synchronization with SpaceflightNewsAPI  |
| GET    | `/reports/sync/progress` | Get sync progress                              |
| POST   | `/reports/sync/cancel`   | Cancel synchronization                         |
| GET    | `/reports/`              | Get articles                                   |
