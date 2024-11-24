from functools import wraps
from flask import session, redirect, url_for, request

def login_required(f):
    """To use on specific enpoints to restrict to only be used when logged in

    Args:
        f (function): The function to wrap

    Returns:
        function: The wrapped function
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:  # check if user_id is in the session
            return redirect(url_for('oauth_bp.authorize', next=request.url))  # redirect to login page
        return f(*args, **kwargs)
    return wrapper
