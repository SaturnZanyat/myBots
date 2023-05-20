from django.contrib import admin
from django.urls import path

from ..testdb import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('quest/', views.RandomQuest.as_view()),
]