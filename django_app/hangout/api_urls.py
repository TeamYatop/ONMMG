from django.urls import path

from . import api_views as views

urlpatterns = [
    path('detail/<str:slug>', views.hangout_detail, name='detail'),
    path('search', views.hangout_search, name='search'),
    path('tags', views.hangout_tags, name='tags'),
    path('areas', views.hangout_areas, name='areas'),
]
