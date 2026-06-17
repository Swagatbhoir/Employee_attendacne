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
    active_employees = Employee.objects.filter(status=Employee.STATUS_ACTIVE).count()
    inactive_employees = total_employees - active_employees

    # Machine statistics
    total_machines = Machine.objects.count()
    active_machines = Machine.objects.filter(status=Machine.STATUS_ACTIVE).count()

    # Attendance statistics for today
    today_records = Attendance.objects.filter(date=today)
    present_today = today_records.filter(attendance_status=Attendance.PRESENT).count()
    absent_today = today_records.filter(attendance_status=Attendance.ABSENT).count()
    leave_today = today_records.filter(attendance_status=Attendance.LEAVE).count()
    half_day_today = today_records.filter(attendance_status=Attendance.HALF_DAY).count()
    marked_today = today_records.count()

    # Quick summary - today's attendance percentage
    # "Present" counts as full attendance, "Half Day" counts as half attendance
    if active_employees:
        attendance_percentage = round(
            ((present_today + (half_day_today * 0.5)) / active_employees) * 100, 1
        )
    else:
        attendance_percentage = 0

    not_marked_today = max(active_employees - marked_today, 0)

    recent_attendance = (
        Attendance.objects.select_related('employee', 'machine')
        .order_by('-date', '-created_at')[:8]
    )

    context = {
        'today': today,
        'total_employees': total_employees,
        'active_employees': active_employees,
        'inactive_employees': inactive_employees,
        'total_machines': total_machines,
        'active_machines': active_machines,
        'inactive_machines': total_machines - active_machines,
        'present_today': present_today,
        'absent_today': absent_today,
        'leave_today': leave_today,
        'half_day_today': half_day_today,
        'marked_today': marked_today,
        'not_marked_today': not_marked_today,
        'attendance_percentage': attendance_percentage,
        'recent_attendance': recent_attendance,
    }
    return render(request, 'dashboard/home.html', context)
