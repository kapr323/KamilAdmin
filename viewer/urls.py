from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from viewer.views import *
from viewer.views import personnel_management

urlpatterns = ([
    path('', home, name='home'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('assign-section/', section_view, name='assign_section'),
    path('about/', about, name='about'),
    path('settings/', user_settings, name='user_settings'),
    path('favorite/', user_favorite, name='user_favorite'),
    path('account/', user_account, name='user_account'),
    path('reservation-system/vehicles', vehicles_reservations, name='reservation_system_vehicles'),
    path('reservation-system/properties', properties_reservations, name='reservation_system_properties'),
    path('organizational-structure/', organizational_structure, name='organizational_structure'),
    path('internal-directives/', internal_directives, name='internal_directives'),
    path('internal-directives/add/', directive_create, name='directive_create'),
    path('upload/internal-directive/<int:pk>/', upload_internal_directive, name='upload_internal_directive'),
    path('internal-directive/<int:pk>/', directive_detail, name='internal_directive_detail'),
    path('internal-directives/edit/<int:pk>/', directive_update, name='directive_update'),
    path('internal-directives/delete/<int:pk>/', directive_delete, name='directive_delete'),
    path('internal-directives/detail/<int:pk>/', directive_detail, name='directive_detail'),
    path('personnel-records/', personnel_records, name='personnel_records_table'),
    path('personnel-records/add/', add_employee, name='add_employee'),
    path('personnel-records/edit/<int:pk>/', employee_update, name='employee_update'),
    path('personnel-records/delete/<int:pk>/', employee_delete, name='employee_delete'),
    path('personnel-records/detail/<int:pk>/', employee_detail, name='employee_detail'),
    path('agreement-workers/', agreement_workers_list, name='agreement_workers_list'),
    path('agreement-workers/add/', add_agreement_worker, name='add_agreement_worker'),
    path('agreement-workers/edit/<int:pk>/', agreement_worker_update, name='agreement_worker_update'),
    path('agreement-workers/delete/<int:pk>/', agreement_worker_delete, name='agreement_worker_delete'),
    path('agreement-workers/<int:pk>/', agreement_worker_detail, name='agreement_worker_detail'),
    path('properties/', properties_table, name='properties_table'),
    path('properties/add/', property_create, name='property_create'),
    path('properties/edit/<int:pk>/', property_update, name='property_update'),
    path('properties/delete/<int:pk>/', property_delete, name='property_delete'),
    path('properties/detail/<int:pk>/', properties_detail, name='properties_detail'),
    path('vehicles/', vehicles_table, name='vehicles_table'),
    path('vehicles/add/', vehicle_create, name='vehicle_create'),
    path('vehicles/edit/<int:pk>/', vehicle_update, name='vehicle_update'),
    path('vehicles/delete/<int:pk>/', vehicle_delete, name='vehicle_delete'),
    path('vehicles/<int:pk>/', vehicle_detail, name="vehicle_detail"),
    path('employee/<int:employee_pk>/competence/<int:competence_pk>/upload/', upload_employee_certificate, name='upload_employee_certificate'),
    path('personalistika/', personnel_management, name='personnel_management'),
    path('nemovitosti/', properties, name='properties'),
    path('vozidla/', vehicles, name='vehicles'),
])

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Všechny soubory v adresáři media, budou dostupné na URL, která začíná /media/