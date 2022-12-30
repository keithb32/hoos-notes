
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from scheduler import views

urlpatterns = [
    path('', include('scheduler.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
]
