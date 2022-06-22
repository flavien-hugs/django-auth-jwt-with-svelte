
# backend.urls.py

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('api/', include('accounts.urls', namespace='accounts')),
    path('admin/', admin.site.urls),
]
