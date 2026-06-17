import csv
import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import render

from attendance.models import Attendance
from employees.models import Employee
from machines.models import Machine

from .forms import AttendanceReportFilterForm, DateRangeForm


def _apply_date_range(queryset, form, date_field='date'):
    start = form.cleaned_data.get('start_date') if form.is_valid() else None
    end = form.cleaned_data.get('end_date') if form.is_valid() else None
    if start:
        queryset = queryset.filter(**{f'{date_field}__gte': start})
    if end:
        queryset = queryset.filter(**{f'{date_field}__lte': end})
    return queryset, start, end


@login_required
def employee_report(request):
    form = DateRangeForm(request.GET or None)
    attendance_qs = Attendance.objects.all()
    attendance_qs, start, end = _apply_date_range(attendance_qs, form)

    employees = Employee.objects.all().order_by('employee_id')

    report_rows = []
    for employee in employees:
        records = attendance_qs.filter(employee=employee)
        report_rows.append({
            'employee': employee,
            'present': records.filter(attendance_status=Attendance.PRESENT).count(),
            'absent': records.filter(attendance_status=Attendance.ABSENT).count(),
            'leave': records.filter(attendance_status=Attendance.LEAVE).count(),
            'half_day': records.filter(attendance_status=Attendance.HALF_DAY).count(),
            'total': records.count(),
        })

    context = {
        'form': form,
        'report_rows': report_rows,
        'start_date': start,
        'end_date': end,
    }
    return render(request, 'reports/employee_report.html', context)


@login_required
def machine_usage_report(request):
    form = DateRangeForm(request.GET or None)
    attendance_qs = Attendance.objects.filter(machine__isnull=False)
    attendance_qs, start, end = _apply_date_range(attendance_qs, form)

    today = datetime.date.today()
    month_start = today.replace(day=1)

    machines = Machine.objects.all().order_by('machine_id')

    report_rows = []
    for machine in machines:
        records = attendance_qs.filter(machine=machine)
        report_rows.append({
            'machine': machine,
            'total_employees_assigned': records.values('employee').distinct().count(),
            'daily_usage': records.filter(date=today).count(),
            'monthly_usage': records.filter(date__gte=month_start, date__lte=today).count(),
            'total_usage': records.count(),
        })

    context = {
        'form': form,
        'report_rows': report_rows,
        'start_date': start,
        'end_date': end,
        'today': today,
    }
    return render(request, 'reports/machine_usage_report.html', context)


def _filtered_attendance(request):
    form = AttendanceReportFilterForm(request.GET or None)
    records = Attendance.objects.select_related('employee', 'machine').all()

    if form.is_valid():
        start = form.cleaned_data.get('start_date')
        end = form.cleaned_data.get('end_date')
        employee = form.cleaned_data.get('employee')
        machine = form.cleaned_data.get('machine')
        status = form.cleaned_data.get('attendance_status')

        if start:
            records = records.filter(date__gte=start)
        if end:
            records = records.filter(date__lte=end)
        if employee:
            records = records.filter(employee=employee)
        if machine:
            records = records.filter(machine=machine)
        if status:
            records = records.filter(attendance_status=status)

    return form, records.order_by('-date', 'employee__employee_id')


@login_required
def attendance_report(request):
    form, records = _filtered_attendance(request)

    from django.core.paginator import Paginator
    paginator = Paginator(records, 20)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'form': form,
        'page_obj': page_obj,
        'total_count': records.count(),
    }
    return render(request, 'reports/attendance_report.html', context)


@login_required
def export_attendance_csv(request):
    _, records = _filtered_attendance(request)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Employee ID', 'Employee Name', 'Attendance Status', 'Machine', 'Remarks'])
    for record in records:
        writer.writerow([
            record.date,
            record.employee.employee_id,
            record.employee.full_name,
            record.attendance_status,
            record.machine.machine_name if record.machine else '--',
            record.remarks,
        ])
    return response
