"""
URL configuration for project project.

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
from django.urls import path

from main.views import *
from authentification.views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('dash',home),
    #PAge d'accueil
    path("accueil/", accueil,name="accueil"),
    #Connexion
    path("login/", login,name="login"),
    #Inscription
    path("signup/",signup,name='signup'),
    #Profil Utilisateur
    path("utilisateur/",utilisateur,name='utilisateur'),
    
    #Recuperer les types d'evenements sous format JSON pour les afficher avec du JS
    path("typeevent-json/",get_type_event,name='typeeventjson'),
    #Recuperer les dates non disponibles de l'equipe passee en parametres sous format JSON
    path("utilisateur/team-json/<str:typeEvent>/",get_json_team),
    #recuperer les heures dispo d'une date
    #path("utilisateur/hour-json/<str:typeEvent>/<str:appDate>/",get_json_hour),
    path("utilisateur/hour-json/<str:typeEvent>/<str:appDate>/",get_available_hours_for_date),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #Servir les fichiers média à partir de settings.MEDIA_ROOT 





