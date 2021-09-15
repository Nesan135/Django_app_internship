from django.urls import path
from .views import upload_seats,upload_data

app_name = 'csvs'
urlpatterns = [
    path('seats/',upload_seats, name='upload_seats'),
    path('data/',upload_data, name='upload_data'),
]