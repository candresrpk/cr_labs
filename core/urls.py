from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('my_apps.web.urls')),
    path('accounts/', include('my_apps.accounts.urls')),
    path('encuestas/', include('my_apps.encuestas.urls')),
]
