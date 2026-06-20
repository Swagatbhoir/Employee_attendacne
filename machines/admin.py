from django.contrib import admin
from .models import Machine


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('machine_id', 'machine_name', 'machine_number', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('machine_id', 'machine_name', 'machine_number')
    ordering = ('machine_id',)
    list_per_page = 25
    readonly_fields = ('machine_id', 'created_at')
