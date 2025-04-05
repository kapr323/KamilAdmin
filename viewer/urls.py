from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from viewer.forms import section_view
from viewer.views import *

urlpatterns = [
    path('', home, name='home'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('assign-section/', section_view, name='assign_section'),
    path('about/', about, name='about'),
    path('settings/', user_settings, name='user_settings'),
    path('favorite/', user_favorite, name='user_favorite'),
    path('account/', user_account, name='user_account'),
    path('reservation-system/', reservation_system, name='reservation_system'),
    path('organizational-structure/', organizational_structure, name='organizational_structure'),
    path('rooms/', rooms_table, name='rooms_table'),
    path('internal-directives/', internal_directives, name='internal_directives'),
    path('internal-directives/add/', directive_create, name='directive_create'),
    path('internal-directives/edit/<int:pk>/', directive_update, name='directive_update'),
    path('internal-directives/delete/<int:pk>/', directive_delete, name='directive_delete'),
    path('internal-directives/detail/<int:pk>/', directive_detail, name='directive_detail'),
    path('personnel-records/', personnel_records, name='personnel_records'),
    path('personnel-records/add/', employee_create, name='employee_create'),
    path('personnel-records/edit/<int:pk>/', employee_update, name='employee_update'),
    path('personnel-records/delete/<int:pk>/', employee_delete, name='employee_delete'),
    path('personnel-records/detail/<int:pk>/', employee_detail, name='employee_detail'),
    path('properties/', properties_table, name='properties'),
    path('properties/add/', property_create, name='property_create'),
    path('properties/edit/<int:pk>/', property_update, name='property_update'),
    path('properties/delete/<int:pk>/', property_delete, name='property_delete'),
    path('properties/detail/<int:pk>/', properties_detail, name='properties_detail'),
    path('vehicles/', vehicles_table, name='vehicles_table'),
    path('vehicles/add/', vehicle_create, name='vehicle_create'),
    path('vehicles/edit/<int:pk>/', vehicle_update, name='vehicle_update'),
    path('vehicles/delete/<int:pk>/', vehicle_delete, name='vehicle_delete'),
    path('vehicles/<int:pk>/', vehicle_detail, name="vehicle_detail"),
]
