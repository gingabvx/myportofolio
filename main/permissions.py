from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

EDITOR_GROUP = "Editor"
LOGIN_URL = "/login/"


def is_editor(user):
    return user.is_authenticated and user.groups.filter(name=EDITOR_GROUP).exists()


def can_edit(user):
    return user.is_authenticated and (user.is_superuser or is_editor(user))


def can_create_delete(user):
    return user.is_authenticated and user.is_superuser


def role_required(check):
    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url=LOGIN_URL)
        def wrapper(request, *args, **kwargs):
            if not check(request.user):
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


editor_required = role_required(can_edit)
superuser_required = role_required(can_create_delete)
