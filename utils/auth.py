from functools import wraps

from flask import abort
from flask_login import current_user


def role_required(*roles):
    allowed_roles = {r for r in roles if r}

    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            user_role = getattr(current_user, 'role', None)
            if not user_role or user_role not in allowed_roles:
                return abort(403)
            return func(*args, **kwargs)

        return wrapped

    return decorator
