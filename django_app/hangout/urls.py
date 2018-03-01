from django.urls import path

from . import views

urlpatterns = [
    path('', views.HangoutDefaultListView.as_view(), name='default'),
    path('<str:tags>', views.HangoutListView.as_view(), name='list'),
]
