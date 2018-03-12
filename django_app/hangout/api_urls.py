from django.urls import path

from . import api_views as views

urlpatterns = [
    path('', views.hangout_list, name='list'),
    path('<int:pk>', views.hangout_detail, name='detail'),
    path('<str:words>', views.hangout_search_list, name='search'),
]
