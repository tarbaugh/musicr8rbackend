from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('reg/', views.registration, name='registration'),
    path('songret/', views.songret, name='songret'),
    path('artistret/', views.artistret, name='artistret'),
    path('rate/', views.rate, name="rate"),
    path('getallsongs/', views.getallsongs, name="getallsongs"),
    path('deletesong/', views.deletesong, name="deletesong"),
]