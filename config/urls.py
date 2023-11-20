"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('help', views.help_page, name='help'),
    path('dictionary/', include('dictionary.urls')),
    path('decks/', include('decks.urls')),
    path('roleplay/', include('roleplay.urls')),
    path("users/register", views.register_request, name="register"),
    path("users/login", views.login_request, name="login"),
    path("users/logout", views.logout_view, name="logout"),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)