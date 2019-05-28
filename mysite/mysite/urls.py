from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from core.views import MatchListView, ModalContent, Login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),

]
