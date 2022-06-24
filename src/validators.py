from typing import List
from flask import redirect, render_template,request, make_response, Response
from functools import wraps
from src.DB_Model import Users, Groups

def canonical_redirect(group : List[Groups] ) -> Response:
    if group == []:
        return make_response(redirect('/'))
    
    if group[0].group == "admin":
        return make_response(redirect('/control'))
    if group[0].group == "analist":
        return make_response(redirect('/dataProducers'))
    else:
        return make_response(redirect('/'))


def check_privileges(valid_groups):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            login    = request.cookies.get('login')
            password = request.cookies.get('password')
            resp = make_response(redirect('/'))
            
            if (not login or not password):
                resp.set_cookie('login', "",0)
                resp.set_cookie('password',"",0)
                return resp
            user = Users.query.filter_by(login=login).first()
            if (not user or user is None):
                resp.set_cookie('login', "",0)
                resp.set_cookie('password',"",0)
                return resp
            resp = canonical_redirect(user.group_user)
            
            if (user.password == password and any([g.group in valid_groups for g in user.group_user])):
                return function(*args, **kwargs)
            else:
                return resp
        return wrapper
    return decorator