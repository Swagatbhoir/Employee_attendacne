import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from employees.models import Employee
from .forms import AttendanceFormSet, DateSelectForm
from .models import Attendance


@login_required
def daily_attendance(request):
    # Determine which date we are marking attendance for
    date_str = request.GET.get('date') or request.POST.get('date')
    if date_str:
        try:
            selected_date = datetime.date.fromisoformat(date_str)
        except ValueError:
            selected_date = datetime.date.today()
    else:
        selected_date = datetime.date.today()

    employees = Employee.objects.all().order_by('employee_id')

    # Existing attendance records for the selected date, keyed by employee pk
    existing_records = {
        record.employee_id: record
        for record in Attendance.objects.filter(date=selected_date, employee__in=employees)
    }

    if request.method == 'POST':
        formset = AttendanceFormSet(request.POST)
        if formset.is_valid():
            saved_count = 0
            for form in formset:
                employee_id = form.cleaned_data['employee_id']
                status = form.cleaned_data['attendance_status']
                machine = form.cleaned_data.get('machine')
                remarks = form.cleaned_data.get('remarks', '')

                Attendance.objects.update_or_create(
                    employee_id=employee_id,
                    date=selected_date,
                    defaults={
                        'attendance_status': status,
                        'machine': machine,
                        'remarks': remarks,
                    }
                )
                saved_count += 1

            messages.success(
                request,
                f'Attendance for {selected_date.strftime("%d %b %Y")} saved successfully '
                f'for {saved_count} employee(s).'
            )
            return redirect(f'/attendance/?date={selected_date.isoformat()}')
        else:
            messages.error(request, 'Please correct the errors highlighted below.')
    else:
        initial_data = []
        for employee in employees:
            record = existing_records.get(employee.employee_id)
            if record:
                initial_data.append({
                    'employee_id': employee.id,
                    'attendance_status': record.attendance_status,
                    'machine': record.machine_id,
                    'remarks': record.remarks,
                })
            else:
                initial_data.append({
                    'employee_id': employee.id,
                    'attendance_status': '',
                    'machine': None,
                    'remarks': '',
                })

        formset = AttendanceFormSet(initial=initial_data)

    date_form = DateSelectForm(initial={'date': selected_date})

    # Pair each employee with its corresponding formset row for template rendering
    rows = list(zip(employees, formset))

    # Quick stats for the selected date
    today_stats = {
        'present': sum(1 for r in existing_records.values() if r.attendance_status == Attendance.PRESENT),
        'absent': sum(1 for r in existing_records.values() if r.attendance_status == Attendance.ABSENT),
        'marked': len(existing_records),
        'total': employees.count(),
    }

    context = {
        'rows': rows,
        'formset': formset,
        'date_form': date_form,
        'selected_date': selected_date,
        'today_stats': today_stats,
    }
    return render(request, 'attendance/daily_attendance.html', context)
