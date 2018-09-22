from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('update/', views.update, name='update'),
    path('replay/', views.replay, name='replay'),
    path('show/', views.show, name='show'),
    path('search/', views.search, name='search'),
    path('filter/', views.filter, name='filter'),
]