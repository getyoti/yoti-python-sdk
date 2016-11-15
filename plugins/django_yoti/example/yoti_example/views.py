from django.shortcuts import render
from django_yoti import yoti_authenticated


def login(request):
    return render(request, 'login.html')


@yoti_authenticated
def profile(request):
    user_profile = request.yoti_user_profile
    return render(request, 'profile.html', user_profile)
