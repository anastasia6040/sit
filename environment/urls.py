from django.urls import path
from .views import home, add_city

urlpatterns = [
    path('', home, name='home'),
    path('add-city/', add_city, name='add_city'),
]
