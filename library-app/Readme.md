# Library Management Web Application

## Overview
Server-rendered Flask application with JWT authentication and role-based authorization.

## Roles
- Admin: manage books
- Member: view available books

## Authentication
- JWT stored in HTTP-only cookies
- Passwords hashed using bcrypt

## Default Admin
Username: admin  
Password: admin123

## Run
pip install -r requirements.txt  
python app.py
