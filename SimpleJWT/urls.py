"""SimpleJWT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from SimpleJWT_app import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from SimpleJWT_app.views import MyObtainTokenPairView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('token', MyObtainTokenPairView.as_view(), name='token'),
    path('refresh', TokenRefreshView.as_view(), name='refresh'),
    path('return_key', views.return_key, name='return_key'),
    path('test_login', views.test_login, name='test_login'),
    path('', views.index, name='index')

]
