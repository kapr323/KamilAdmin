from django.urls import path
from django.contrib import admin
from .views import home
from . import views

urlpatterns = [
    path('', home, name='home'),
    path('about/', views.about, name='about'),
    path('settings/', views.user_settings, name='user_settings'),
    path('favorite/', views.user_favorite, name='user_favorite'),
    path('account/', views.user_account, name='user_account'),
    path('reservation-system/', views.reservation_system, name='reservation_system'),
    path('organizational-structure/', views.organizational_structure, name='organizational_structure'),
    path('personnel-records/', views.personnel_records, name='personnel_records'),
    path('properties/', views.properties_table, name='properties_table'),
    path('rooms/', views.rooms_table, name='rooms_table'),
    path('vehicles/', views.vehicles_table, name='vehicles_table'),
    path('internal-guidelines/', views.internal_guidelines, name='internal_guidelines'),
    path('new/', views.submit_certificate, name='submit_certificate'), # nechat new?
    path('vehicles/<int:car_id>/', views.vehicle_detail, name="vehicle_detail"),
]
