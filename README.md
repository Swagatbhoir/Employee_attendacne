# Employee Attendance & Machine Assignment System

An admin-only web application for managing daily employee attendance and
machine (equipment) assignments, built with **Python 3, Django 5, Bootstrap
5, and SQLite**.

There is **no employee-facing login** — only an administrator (Django
superuser / staff user) signs in to manage employees, machines, attendance,
and reports.

---

## Features

- **Authentication**: Login, Logout, Change Password (admin-only, all pages
  require login).
- **Employee Management**: Add / Edit / Delete / Search / List / Detail view.
  Employee IDs (e.g. `EMP001`) are auto-generated.
- **Machine Management**: Add / Edit / Delete / Search / List. Machine IDs
  (e.g. `MCH001`) are auto-generated.
- **Daily Attendance**: Mark Present / Absent / Leave / Half Day for every
  active employee in a single table and save in one click. Machine
  assignment is **required** for Present / Half Day and disabled for
  Absent / Leave.
- **Dashboard**: Employee, attendance (today), and machine statistics, plus
  today's attendance percentage and recent activity.
- **Reports**:
  - Employee Report (Present / Absent / Leave / Half Day totals, filter by
    date range)
  - Machine Usage Report (employees assigned, daily/monthly usage, filter by
    date range)
  - Attendance Report (filter by date, employee, machine, status)
- **CSV Export**: Attendance Report, Employee List, Machine List.
- **Django Admin**: All models registered with search, filters, ordering and
  bulk actions.
- **Responsive UI**: Bootstrap 5 sidebar layout, mobile-friendly, clean
  corporate light theme.

---

## Project Structure

```
employee_attendance/
├── accounts/             # Login / logout / change password
├── employees/            # Employee CRUD + CSV export + sample data command
├── machines/              # Machine CRUD + CSV export
├── attendance/            # Daily attendance marking & machine assignment
├── dashboard/             # Dashboard with statistics
├── reports/               # Employee / machine usage / attendance reports
├── templates/             # Shared & app templates (Bootstrap 5)
├── static/                 # CSS / JS
├── media/                  # Uploaded media (if any)
├── employee_attendance/   # Project settings, urls, wsgi/asgi
├── manage.py
└── requirements.txt
```

---

## Local Setup

1. **Create and activate a virtual environment** (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**:

   ```bash
   python manage.py migrate
   ```

4. **Create an admin (superuser) account**:

   ```bash
   python manage.py createsuperuser
   ```

5. **(Optional) Load sample data** — sample employees, machines and a week of
   attendance records:

   ```bash
   python manage.py seed_data
   ```

   You can change how many days of attendance history are generated:

   ```bash
   python manage.py seed_data --days 14
   ```

6. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

7. Open `http://127.0.0.1:8000/` and log in with the superuser credentials
   created in step 4.

---

## Key URLs

| Page                  | URL                           |
|-----------------------|--------------------------------|
| Login                 | `/accounts/login/`             |
| Logout                | `/accounts/logout/`            |
| Change Password       | `/accounts/password-change/`   |
| Dashboard             | `/`                             |
| Daily Attendance      | `/attendance/`                 |
| Employees             | `/employees/`                  |
| Machines              | `/machines/`                   |
| Employee Report       | `/reports/employee/`           |
| Machine Usage Report  | `/reports/machine-usage/`      |
| Attendance Report     | `/reports/attendance/`         |
| Django Admin          | `/admin/`                       |

---

## Business Rules

- **One attendance record per employee per date** — re-submitting the daily
  attendance form for the same date updates the existing record instead of
  creating a duplicate.
- If attendance status is **Present** or **Half Day**, a **Machine must be
  selected**.
- If attendance status is **Absent** or **Leave**, the machine field is
  disabled and cleared automatically.
- Only **Active** employees appear on the Daily Attendance screen.
- Only **Active** machines can be assigned during attendance.

---

## Deployment on PythonAnywhere

1. Upload/clone the project to your PythonAnywhere account (e.g. via the
   "Files" tab or `git clone` in a Bash console).

2. Create a virtualenv and install requirements:

   ```bash
   mkvirtualenv --python=python3.11 attendance-env
   pip install -r requirements.txt
   ```

3. In the **Web** tab, create a new web app (Manual configuration, matching
   Python version) and point the virtualenv to `attendance-env`.

4. Edit the WSGI configuration file to point to
   `employee_attendance.wsgi.application` and set the project path, e.g.:

   ```python
   import sys
   path = '/home/<your-username>/employee_attendance'
   if path not in sys.path:
       sys.path.append(path)

   import os
   os.environ['DJANGO_SETTINGS_MODULE'] = 'employee_attendance.settings'

   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

5. Set environment variables (via the Web tab "Environment variables"
   section or a `.env` loader of your choice):

   - `DJANGO_SECRET_KEY` — a long random string
   - `DJANGO_DEBUG` — `False`
   - `DJANGO_ALLOWED_HOSTS` — `<your-username>.pythonanywhere.com`

6. Run migrations and create the superuser from a Bash console (with the
   virtualenv active):

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py collectstatic
   ```

7. In the **Web** tab, map a static files entry:

   - URL: `/static/`
   - Directory: `/home/<your-username>/employee_attendance/staticfiles`

   And for media (optional):

   - URL: `/media/`
   - Directory: `/home/<your-username>/employee_attendance/media`

8. Reload the web app. Visit your PythonAnywhere URL and log in with the
   superuser account.

---

## Notes

- Local development uses **SQLite** (`db.sqlite3`), but production should use
   **PostgreSQL** via `DATABASE_URL`.
- All pages other than the login page require authentication.
- Employee and Machine IDs are generated automatically (`EMP001`, `MCH001`,
  ...) and are not editable from the UI.
