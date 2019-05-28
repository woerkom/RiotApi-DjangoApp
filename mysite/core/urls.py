from django.contrib import admin
from django.urls import path
from .views import MatchListView, ModalContent, Login
urlpatterns = [
    path('matches/', MatchListView, name='boostrap'),
    path('', Login, name='login'),
    path('content/<int:gameId>/', ModalContent, name='modalContent')
]

##todo esto creado como prueba