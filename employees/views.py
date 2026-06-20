import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from attendance.models import Attendance
from .forms import EmployeeForm, EmployeeSearchForm
from .models import Employee


@login_required
def employee_list(request):
    employees = Employee.objects.all()
    search_form = EmployeeSearchForm(request.GET or None)

    if search_form.is_valid():
        query = search_form.cleaned_data.get('q')

        if query:
            employees = employees.filter(
                Q(employee_id__icontains=query) | Q(full_name__icontains=query)
            )

    paginator = Paginator(employees, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'total_count': employees.count(),
    }
    return render(request, 'employees/employee_list.html', context)


@login_required
def employee_add(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save()
            messages.success(
                request, f'Employee "{employee.full_name}" ({employee.employee_id}) added successfully.'
            )
            return redirect('employees:list')
    else:
        form = EmployeeForm()

    return render(request, 'employees/employee_form.html', {
        'form': form,
        'title': 'Add Employee',
    })


@login_required
def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, f'Employee "{employee.full_name}" updated successfully.')
            return redirect('employees:list')
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'employees/employee_form.html', {
        'form': form,
        'title': 'Edit Employee',
        'employee': employee,
    })


@login_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        name = f'{employee.full_name} ({employee.employee_id})'
        employee.delete()
        messages.success(request, f'Employee "{name}" deleted successfully.')
        return redirect('employees:list')

    return render(request, 'employees/employee_confirm_delete.html', {'employee': employee})


@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    attendance_records = Attendance.objects.filter(employee=employee).select_related('machine').order_by('-date')[:30]

    summary = {
        'present': Attendance.objects.filter(employee=employee, attendance_status=Attendance.PRESENT).count(),
        'absent': Attendance.objects.filter(employee=employee, attendance_status=Attendance.ABSENT).count(),
    }

    return render(request, 'employees/employee_detail.html', {
        'employee': employee,
        'attendance_records': attendance_records,
        'summary': summary,
    })


@login_required
def export_employees_csv(request):
    employees = Employee.objects.all().order_by('employee_id')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employee_list.csv"'

    writer = csv.writer(response)
    writer.writerow(['Employee ID', 'Full Name', 'Mobile Number', 'Status', 'Created Date'])
    for employee in employees:
        writer.writerow([
            employee.employee_id,
            employee.full_name,
            employee.mobile_number,
            employee.status,
            employee.created_at.strftime('%Y-%m-%d'),
        ])
    return response
