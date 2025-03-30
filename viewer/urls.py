from django.contrib import admin
from django.urls import path

from viewer.forms import section_view
from viewer.views import *

urlpatterns = [
    path('', home, name='home'),

    path('assign-section/', section_view, name='assign_section'),
]
