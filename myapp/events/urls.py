from django.contrib import admin
from django.urls import include, path
from .admin import CustomAdminSite

admin_site = CustomAdminSite()



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('events.urls')),
    # Other URL patterns
]
                              