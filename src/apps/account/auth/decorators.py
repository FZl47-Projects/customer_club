from functools import wraps
from django.core.exceptions import PermissionDenied


def user_role_required_cbv(roles):
    def wrapper(func):
        @wraps(func)
        def inner(self, request, *args, **kwargs):
            user = request.user
            if user is None or user.is_anonymous:
                raise PermissionDenied
            role = user.role
            if not (role in roles):
                raise PermissionDenied
            return func(self, request, *args, **kwargs)

        return inner

    return wrapper
