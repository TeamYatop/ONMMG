from django.urls import path

from . import views

urlpatterns = [
    path('', views.HangoutSearchView.as_view(), name='default'),
]
