from django.contrib import admin
from django.urls import path
from .views import MatchListView, ModalContent, Login, Estadisticas
urlpatterns = [
    path('matches/', MatchListView, name='matches'),
    path('', Login, name='login'),
    path('content/<int:gameId>/', ModalContent, name='modalContent'),
    path('estadisticas', Estadisticas, name='estadisticas')
]

##todo esto creado como prueba