import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from attendance.models import Attendance
from employees.models import Employee
from machines.models import Machine


@login_required
def home(request):
    today = datetime.date.today()

    # Employee statistics
    total_employees = Employee.objects.count()

    # Machine statistics
    total_machines = Machine.objects.count()

    # Attendance statistics for today
    today_records = Attendance.objects.filter(date=today)
    present_today = today_records.filter(attendance_status=Attendance.PRESENT).count()
    absent_today = today_records.filter(attendance_status=Attendance.ABSENT).count()
    marked_today = today_records.count()

    # Quick summary - today's attendance percentage
    if total_employees:
        attendance_percentage = round(
            (present_today / total_employees) * 100, 1
        )
    else:
        attendance_percentage = 0

    not_marked_today = max(total_employees - marked_today, 0)

    recent_attendance = (
        Attendance.objects.select_related('employee', 'machine')
        .order_by('-date', '-created_at')[:8]
    )

    context = {
        'today': today,
        'total_employees': total_employees,
        'total_machines': total_machines,
        'present_today': present_today,
        'absent_today': absent_today,
        'marked_today': marked_today,
        'not_marked_today': not_marked_today,
        'attendance_percentage': attendance_percentage,
        'recent_attendance': recent_attendance,
    }
    return render(request, 'dashboard/home.html', context)
