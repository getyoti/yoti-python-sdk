from functools import wraps

from django.shortcuts import redirect
from django.urls import reverse

from .settings import YOTI_LOGIN_VIEW


def yoti_authenticated(view_func):
    @wraps(view_func)
    def _decorated(request, *args, **kwargs):
        activity_details = request.session.get('activity_details')
        if not activity_details or activity_details.get('outcome') != 'SUCCESS':
            return redirect(reverse(YOTI_LOGIN_VIEW))

        yoti_user_id = activity_details.get('user_id')
        yoti_user_profile = activity_details.get('user_profile')
        setattr(request, 'yoti_user_id', yoti_user_id)
        setattr(request, 'yoti_user_profile', yoti_user_profile)

        return view_func(request, *args, **kwargs)

    return _decorated
