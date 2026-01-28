from flask import request, redirect, url_for, g, flash
import jwt
import datetime
from functools import wraps
from database import get_db
import bcrypt
from flask import current_app as app

def create_jwt(user_id, username, role):
    payload = {
        "user_id": user_id,
        "username": username,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    token = jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")
    return token

def decode_jwt(token):
    try:
        return jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    except:
        return None

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = request.cookies.get("access_token")
        if not token:
            return redirect(url_for("login"))
        decoded = decode_jwt(token)
        if not decoded:
            return redirect(url_for("login"))
        g.user = {
            "id": decoded["user_id"],
            "username": decoded["username"],
            "role": decoded["role"]
        }
        return fn(*args, **kwargs)
    return wrapper

def role_required(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not g.user or g.user["role"] != role:
                flash("Unauthorized access!")
                return redirect(url_for("login"))
            return fn(*args, **kwargs)
        return wrapper
    return decorator
