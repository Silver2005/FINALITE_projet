from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from gest_demande import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('demande/', views.nouvelle_demande, name='nouvelle_demande'),
    path('quittance/<int:demande_id>/', views.generer_quittance, name='generer_quittance'),

    # URLS POUR LA CONNEXION ET LA DÉCONNEXION
    path('accounts/login/', auth_views.LoginView.as_view(template_name='gest_demande/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]