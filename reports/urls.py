from django.urls import path

from . import views

app_name = 'reports'

urlpatterns = [
    path('employee/', views.employee_report, name='employee_report'),
    path('machine-usage/', views.machine_usage_report, name='machine_usage_report'),
    path('attendance/', views.attendance_report, name='attendance_report'),
    path('attendance/export/', views.export_attendance_csv, name='export_attendance_csv'),
]
