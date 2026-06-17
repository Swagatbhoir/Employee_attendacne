from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'full_name', 'mobile_number', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('employee_id', 'full_name', 'mobile_number')
    ordering = ('employee_id',)
    list_per_page = 25
    actions = ['mark_active', 'mark_inactive']
    readonly_fields = ('employee_id', 'created_at')

    @admin.action(description='Mark selected employees as Active')
    def mark_active(self, request, queryset):
        updated = queryset.update(status=Employee.STATUS_ACTIVE)
        self.message_user(request, f'{updated} employee(s) marked as Active.')

    @admin.action(description='Mark selected employees as Inactive')
    def mark_inactive(self, request, queryset):
        updated = queryset.update(status=Employee.STATUS_INACTIVE)
        self.message_user(request, f'{updated} employee(s) marked as Inactive.')
