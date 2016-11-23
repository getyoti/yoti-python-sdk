from yoti import Client
from django.shortcuts import render, redirect
from django.urls import reverse

from .decorators import yoti_authenticated
from .settings import (
    YOTI_CLIENT_SDK_ID,
    YOTI_KEY_FILE_PATH,
    YOTI_REDIRECT_TO,
)


def login(request):
    return render(request, 'yoti_login.html')


def auth(request):
    token = request.GET.get('token')
    if not token:
        return render(request, 'yoti_auth.html')

    client = Client(YOTI_CLIENT_SDK_ID, YOTI_KEY_FILE_PATH)
    activity_details = client.get_activity_details(token)
    request.session['activity_details'] = dict(activity_details)
    return redirect(reverse(YOTI_REDIRECT_TO))


@yoti_authenticated
def profile(request):
    user_profile = request.yoti_user_profile
    return render(request, 'yoti_profile.html', user_profile)
