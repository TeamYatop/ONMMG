from django.urls import path

from . import api_views as views

urlpatterns = [
    path('<str:slug>', views.hangout_detail, name='detail'),
    path('search/', views.hangout_list, name='search'),
    path('search/<str:words>', views.hangout_search_by_tags, name='search-all-tags'),
    path('search/<str:area>/<str:words>', views.hangout_search_by_area_n_tags, name='search-tags-with-area'),
]
