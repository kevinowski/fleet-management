from django.urls import path
from . import views

urlpatterns = [
    path("", views.starting_page, name="starting-page"),
    path("new-car", views.add_car, name="add-car"),
    path('car/<slug:slug>', views.car_details, name="car-detail"),
    path('car/delete/<str:slug>', views.delete_car, name='delete-car'),
    path('refuel', views.refuel, name='refuel-car'),
    path('report', views.report, name='report'),
    path('service/done/<id>', views.service_done, name="service-done"),
    path('services', views.services, name="services"),

    path('register', views.register_user, name="register"),
    path('login', views.login_user, name="login"),
    path('logout', views.logout_user, name="logout"),
  
]
