from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_route, name='add_route'),
    path('search-nth/', views.search_nth, name='search_nth'),
    path('shortest-path/', views.shortest_path_view, name='shortest_path'),
]
