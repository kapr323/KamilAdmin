from django.urls import path
from . import views


urlpatterns = [
    path('accounts/login/', views.custom_login, name='login'),
    path('change-password/', views.change_password, name='change_password'),   # URL pro změnu hesla
    path('home/', views.home, name='home'),  # Domovská stránka,
]