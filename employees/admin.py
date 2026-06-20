from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'full_name', 'mobile_number', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('employee_id', 'full_name', 'mobile_number')
    ordering = ('employee_id',)
    list_per_page = 25
    readonly_fields = ('employee_id', 'created_at')
