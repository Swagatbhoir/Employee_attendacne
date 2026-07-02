"""
URL configuration for employee_attendance project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('secure-admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('employees/', include('employees.urls')),
    path('machines/', include('machines.urls')),
    path('attendance/', include('attendance.urls')),
    path('reports/', include('reports.urls')),
    path('', include('dashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
