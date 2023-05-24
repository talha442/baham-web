from django.urls import path
from django.contrib.auth.views import LoginView
from . import views


urlpatterns = [
    path('', views.view_home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('baham/vehicles', views.view_vehicles, name='vehicles'),
    path('baham/vehicles/create', views.create_vehicle, name='createvehicle'),
    path('baham/vehicles/save/', views.save_vehicle, name='savevehicle'),
    path('baham/vehicles/delete/<str:uuid>', views.delete_vehicle, name='deletevehicle'),
    path('baham/vehicles/edit/<str:uuid>', views.edit_vehicle, name='editvehicle'),
    path('baham/vehicles/edit/update/', views.update_vehicle, name='updatedvehicle'),
    path('baham/aboutus', views.view_aboutus, name='aboutus'),
    
    # REST API
    path('api/get_csrf_token', views.get_csrf_token, name='get_csrf_token'),
    path('api/get/vehicles', views.get_all_vehicle_models, name='get_all_vehicles'),
    path('api/get/vehicles/<str:uuid>', views.get_vehicle_model_by_uuid, name='get_vehicle_model_by_uuid'),
    path('api/create/vehicles', views.create_vehicle_model, name='create_vehicle_model'),
    path('api/updated/vehicles/<str:uuid>', views.update_vehicle_model, name='update_vehicle_model'),
    path('api/delete/vehicles/<str:uuid>', views.delete_vehicle_model, name='delete_vehicle_model'),

]
