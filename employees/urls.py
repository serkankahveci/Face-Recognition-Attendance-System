from django.urls import path
from .views import register_employee  # Eğer böyle bir view'in varsa!

urlpatterns = [
    path('register/', register_employee, name='register_employee'),
]
