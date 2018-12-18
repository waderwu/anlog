from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('replay/', views.replay, name='replay'),
    path('show/', views.show, name='show'),
    path('search/', views.search, name='search'),
    path('stat/', views.statistics, name='stat'),
    path('forward/', views.forward, name='forward')
]