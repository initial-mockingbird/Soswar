from flask import redirect, render_template,request, make_response
from functools import wraps
from src.DB_Model import Users

def check_privileges(valid_groups):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            login    = request.cookies.get('login')
            password = request.cookies.get('password')
            resp = make_response(redirect('/'))
            resp.set_cookie('login', "",0)
            resp.set_cookie('password',"",0)
            if (not login or not password):
                return resp
            user = Users.query.filter_by(login=login).first()
            if (not user or user is None):
                return resp
            if (user.password == password and any([g.group in valid_groups for g in user.group_user])):
                return function(*args, **kwargs)
            else:
                return resp
        return wrapper
    return decorator