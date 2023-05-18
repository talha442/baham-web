from django.urls import path
from . import views


urlpatterns = [
    path('', views.view_home, name='home'),
    path('baham/vehicles', views.view_vehicles, name='vehicles'),
    path('baham/vehicles/create', views.create_vehicle, name='createvehicle'),
    path('baham/vehicles/save/', views.save_vehicle, name='savevehicle'),
    path('baham/vehicles/delete/<str:uuid>', views.delete_vehicle, name='deletevehicle'),
    path('baham/vehicles/edit/<str:uuid>', views.edit_vehicle, name='editvehicle'),
    path('baham/vehicles/edit/update/', views.update_vehicle, name='updatevehicle'),
    path('baham/aboutus', views.view_aboutus, name='aboutus'),
]
