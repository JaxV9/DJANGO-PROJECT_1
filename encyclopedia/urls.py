from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.titles, name="entry"),
    path("newpage", views.newpage, name="newpage"),
    path("mod/<str:title>", views.mod, name="mod"),
    path("random", views.random, name="random")
]
