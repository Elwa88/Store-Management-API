from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/',include('userauth.urls')),
    path('api/warehouse/', include('warehouse.urls')),
]
