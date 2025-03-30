from django.contrib import admin
from django.urls import path

from viewer.forms import section_view
from viewer.views import *

urlpatterns = [
    path('', home, name='home'),

    path('assign-section/', section_view, name='assign_section'),
    path('about/', about, name='about'),
    path('settings/', user_settings, name='user_settings'),
    path('favorite/', user_favorite, name='user_favorite'),
    path('account/', user_account, name='user_account'),
    path('reservation-system/', reservation_system, name='reservation_system'),
    path('organizational-structure/', organizational_structure, name='organizational_structure'),
    path('personnel-records/', personnel_records, name='personnel_records'),
    path('properties/', properties_table, name='properties_table'),
    path('rooms/', rooms_table, name='rooms_table'),
    path('vehicles/', vehicles_table, name='vehicles_table'),
    path('internal-guidelines/', internal_guidelines, name='internal_guidelines'),
    path('new/', submit_certificate, name='submit_certificate'), # nechat new?
    path('vehicles/<int:car_id>/', vehicle_detail, name="vehicle_detail"),
]
