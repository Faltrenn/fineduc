"""fineduc URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
import myapp.views as myapp

urlpatterns = [
    path('', myapp.redirect_index),
    path('getCities/', myapp.getCities, name="get"),
    path('admin/', admin.site.urls),
    path('index/', myapp.index, name="index"),
    path('register/', myapp.register, name="register"),
    path('login/', myapp.login, name="login"),
    path('logout/', myapp.logout, name="logout"),
    path('request/', myapp.request, name="request"),
    path('profile/', myapp.profile, name="profile"),
    path('seeProfile/', myapp.seeProfile, name="seeProfile"),
]

if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  
