from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # Nouvelle URL pour la page d'accueil
    path('demande/', views.nouvelle_demande, name='nouvelle_demande'),
    path('quittance/<int:demande_id>/', views.generer_quittance, name='generer_quittance'),
]