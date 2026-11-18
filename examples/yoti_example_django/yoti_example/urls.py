"""yoti_example URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import re_path
from django.contrib import admin

from .views import IndexView, AuthView, DynamicShareView, SourceConstraintsView

urlpatterns = [
    re_path(r"^$", IndexView.as_view(), name="index"),
    re_path(r"^yoti/auth/$", AuthView.as_view(), name="auth"),
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^dynamic-share/$", DynamicShareView.as_view(), name="dynamic-share"),
    re_path(
        r"^source-constraint/$",
        SourceConstraintsView.as_view(),
        name="source-constraints",
    ),
]
