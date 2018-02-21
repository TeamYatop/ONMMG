from django.urls import path
from . import views


urlpatterns = [
    path('', views.HangoutListView.as_view(), name='list'),
]
