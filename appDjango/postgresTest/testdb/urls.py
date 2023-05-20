from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('quest/', views.RandomQuest.as_view()),
    path('next/<int:pk>', views.NextQuest.as_view())
]
