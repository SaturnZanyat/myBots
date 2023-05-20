from django.contrib import admin
from django.urls import path, include

# from appDjango.postgresTest.testdb import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('testdb.urls')),
    # path('quest/', views.RandomQuest.as_view()),
    # path('next/<int:pk>', views.NextQuest.as_view())
]
