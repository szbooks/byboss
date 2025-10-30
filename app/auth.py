from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash("请先登录！")
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function
