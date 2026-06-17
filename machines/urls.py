from django.urls import path
from . import views

app_name = 'machines'

urlpatterns = [
    path('', views.machine_list, name='list'),
    path('add/', views.machine_add, name='add'),
    path('export/', views.export_machines_csv, name='export_csv'),
    path('<int:pk>/edit/', views.machine_edit, name='edit'),
    path('<int:pk>/delete/', views.machine_delete, name='delete'),
]
