from django.contrib import admin
from django.urls import path
from core.views import MatchListView, Content
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MatchListView, name='boostrap'),
    path('content/', Content, name='content')
]
