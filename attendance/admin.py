from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'attendance_status', 'machine', 'remarks', 'created_at')
    list_filter = ('attendance_status', 'date', 'machine')
    search_fields = ('employee__employee_id', 'employee__full_name', 'remarks')
    date_hierarchy = 'date'
    ordering = ('-date', 'employee__employee_id')
    list_per_page = 25
    autocomplete_fields = ['employee', 'machine']

    fieldsets = (
        (None, {
            'fields': ('employee', 'date', 'attendance_status', 'machine', 'remarks')
        }),
    )
