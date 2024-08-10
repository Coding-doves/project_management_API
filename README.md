# Project Management API

## Overview

This project is a RESTful API for managing tasks and user roles in a project management application. It includes endpoints for user registration, authentication, and task management, with role-based access control for different actions.

## Features

- User registration and authentication
- Role management (admin, user, guest)
- Task creation, retrieval, updating, and deletion
- OAuth2 authentication with JWT tokens

## Technologies

- **FastAPI**: For building the API
- **SQLAlchemy**: For ORM and database management
- **SQLite**: Database for development
- **Passlib**: For password hashing
- **PyJWT**: For handling JSON Web Tokens (JWT)
- **Uvicorn**: ASGI server for running the app

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Coding-doves/project_management_API.git
   cd project_management_API
