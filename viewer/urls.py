from django.urls import path
from .views import home
from . import views

urlpatterns = [
    path('', home, name='home'),
    path('about/', views.about, name='about'),
    path('settings/', views.user_settings, name='user_settings'),
    path('favorite/', views.user_favorite, name='user_favorite'),
    path('account/', views.user_account, name='user_account'),
    path('reservation-system/', views.reservation_system, name='reservation_system'),
]
