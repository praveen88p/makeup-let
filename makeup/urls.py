from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('receive_frame/', views.receive_frame, name='receive_frame'),
]
