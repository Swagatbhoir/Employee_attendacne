import datetime
import random

from django.core.management.base import BaseCommand

from attendance.models import Attendance
from employees.models import Employee
from machines.models import Machine


SAMPLE_EMPLOYEES = [
    ('Rahul Sharma', '9876543210'),
    ('Amit Kumar', '9876543211'),
    ('Suresh Patil', '9876543212'),
    ('Vijay Singh', '9876543213'),
    ('Ramesh Yadav', '9876543214'),
    ('Sandeep Joshi', '9876543215'),
    ('Manoj Verma', '9876543216'),
    ('Deepak Gupta', '9876543217'),
]

SAMPLE_MACHINES = [
    ('Excavator 01', 'EXC-001', 'Excavator'),
    ('Excavator 02', 'EXC-002', 'Excavator'),
    ('JCB 01', 'JCB-001', 'JCB'),
    ('Crane 01', 'CRN-001', 'Crane'),
    ('Loader 01', 'LDR-001', 'Loader'),
]


class Command(BaseCommand):
    help = 'Populate the database with sample employees, machines and attendance records.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=7,
            help='Number of past days (including today) to generate attendance records for.',
        )

    def handle(self, *args, **options):
        days = options['days']

        # --- Employees ---
        employees = []
        for name, mobile in SAMPLE_EMPLOYEES:
            employee, created = Employee.objects.get_or_create(
                full_name=name,
                defaults={'mobile_number': mobile, 'status': Employee.STATUS_ACTIVE},
            )
            employees.append(employee)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created employee {employee.employee_id} - {employee.full_name}'))

        # --- Machines ---
        machines = []
        for name, number, machine_type in SAMPLE_MACHINES:
            machine, created = Machine.objects.get_or_create(
                machine_number=number,
                defaults={
                    'machine_name': name,
                    'machine_type': machine_type,
                    'status': Machine.STATUS_ACTIVE,
                },
            )
            machines.append(machine)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created machine {machine.machine_id} - {machine.machine_name}'))

        # --- Attendance ---
        statuses = [
            Attendance.PRESENT,
            Attendance.PRESENT,
            Attendance.PRESENT,
            Attendance.HALF_DAY,
            Attendance.ABSENT,
            Attendance.LEAVE,
        ]
        active_machines = [m for m in machines if m.status == Machine.STATUS_ACTIVE]

        today = datetime.date.today()
        created_count = 0
        for day_offset in range(days):
            attendance_date = today - datetime.timedelta(days=day_offset)
            for employee in employees:
                if employee.status != Employee.STATUS_ACTIVE:
                    continue

                status = random.choice(statuses)
                machine = None
                if status in Attendance.MACHINE_REQUIRED_STATUSES and active_machines:
                    machine = random.choice(active_machines)

                _, created = Attendance.objects.get_or_create(
                    employee=employee,
                    date=attendance_date,
                    defaults={
                        'attendance_status': status,
                        'machine': machine,
                        'remarks': '',
                    }
                )
                if created:
                    created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Done. Employees: {len(employees)}, Machines: {len(machines)}, '
            f'Attendance records created: {created_count}.'
        ))
