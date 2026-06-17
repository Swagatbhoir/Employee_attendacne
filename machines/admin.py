from django.contrib import admin
from .models import Machine


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('machine_id', 'machine_name', 'machine_number', 'machine_type', 'status', 'created_at')
    list_filter = ('status', 'machine_type', 'created_at')
    search_fields = ('machine_id', 'machine_name', 'machine_number')
    ordering = ('machine_id',)
    list_per_page = 25
    actions = ['mark_active', 'mark_inactive']
    readonly_fields = ('machine_id', 'created_at')

    @admin.action(description='Mark selected machines as Active')
    def mark_active(self, request, queryset):
        updated = queryset.update(status=Machine.STATUS_ACTIVE)
        self.message_user(request, f'{updated} machine(s) marked as Active.')

    @admin.action(description='Mark selected machines as Inactive')
    def mark_inactive(self, request, queryset):
        updated = queryset.update(status=Machine.STATUS_INACTIVE)
        self.message_user(request, f'{updated} machine(s) marked as Inactive.')
