# from django.conf.urls import url
from django.urls import path
from .views import (
    PredictionListApiView,
    PredictionDetailApiView
)

urlpatterns = [
    path('predictions/', PredictionListApiView.as_view(), name='predictions'),
    path('predictions/<int:pk>/', PredictionDetailApiView.as_view(), name='prediction'),
]