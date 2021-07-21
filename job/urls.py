from django.urls import path
from .views import *


urlpatterns = [
    path('', ListJobView.as_view(), name='index'),
    path('add-job/', CreateJobView.as_view(), name='add-job'),
    path('update-job/<int:pk>/', UpdateJobView.as_view(), name='update-job'),
    path('delete-job/<int:pk>/', DeleteJobView.as_view(), name='delete-job'),
]