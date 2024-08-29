# To-Do RESTful API using python

## Overview

This project is a simple To-Do list RESTful API built using Flask. It implements token authentication using 
JWT and allows users to register, log in, and manage tasks using GET, PUT and POST operations.

## Installation:

- ```pip install -r requirements.txt```
- create a new SQLite database file (instance/todo.db)
- execute create_db.py to allow the application to create the tables automatically into the SQLite database using the models
specified in models.py
- execute run.py to start the server.

## API Endpoints
### Authentication

<b>POST /register:</b> registers a new user.

Request body example: {"username": "yourusername", "password": "yourpassword" }

Response: 
- 201 Created on success
- 400 Bad Request (if the user already exists).

<b>POST /login:</b> Authenticate a user and return a JWT token.

Request body example: { "username": "yourusername", "password": "yourpassword" }

Response: 
- 200 OK on success
- 401 Unauthorized (invalid credentials).

### Task Management (Requires Login)

#### <b>GET /tasks/{id}:</b> Retrieve all tasks for the authenticated user.

Response: 200 (with a list of tasks).

#### <b>POST /tasks:</b> Create a new task.

Request body example: { "title": "Task Title", "description": "Task Description", "completed": false }

Response: 
- 201 Created on success
- 400 Bad Request (validation errors).

#### GET /tasks/{task_id}: Retrieve a task by its ID.

Response: 200 OK on success, 404 Not Found if the task does not exist.

#### PUT /tasks/{task_id}: Update an existing task.

Request body example : { "title": "New Title", "description": "New Description", "completed": true }

Response: 
- 200 OK on success
- 400 Bad Request (validation errors).

#### DELETE /tasks/{task_id}: Delete a task by its ID.

Response: 
- 200
- 404 Not Found (if the task does not exist).

## Testing

you can run the included tests using the command:

``` pytest ```
