# Law Firm Management Portal

Role-based legal case management web application built with Django. The platform streamlines client and advocate onboarding, case lifecycle tracking, hearing updates, document handling, and downloadable case summaries.

## Resume-Ready Summary

Built a full-stack legal operations portal with custom authentication, role-specific workflows, secure document handling, and production deployment support.

### What This Project Demonstrates

- Designed and implemented a custom email-based Django authentication model.
- Built role-based access control (Client vs Advocate) with guarded routes and data scoping.
- Implemented end-to-end case lifecycle features: create/update/delete cases, hearings, tasks, and document uploads.
- Generated dynamic PDF case reports using ReportLab.
- Added signal-driven automation to send change notifications for key model updates.
- Configured production-ready settings for PostgreSQL, WhiteNoise static serving, and Render deployment.

## Core Features

- Secure signup/login using custom `User` model (`AUTH_USER_MODEL = core.User`).
- Post-login role selection and onboarding flows:
	- Client onboarding with profile, ID proof, photo, and signature.
	- Advocate onboarding with enrollment and professional details.
- Client workflows:
	- Create, update, and delete own cases.
	- Track upcoming hearings and task deadlines.
- Advocate workflows:
	- Manage hearings for assigned cases.
	- Upload case documents for assigned matters.
- Case detail view with authorization checks and downloadable PDF summary.
- Dashboard views tailored by role.
- Optional email notifications for updates to tracked business records.

## Tech Stack

- Python 3.11+
- Django 5.x
- PostgreSQL (production + optional local)
- SQLite (local development when `DEBUG=True` and `DATABASE_URL` is not set)
- Gunicorn
- WhiteNoise
- ReportLab
- Pillow

## Architecture

### Backend

- App: `core`
	- Domain models: users, profiles, cases, hearings, documents, tasks.
	- Forms with validation and onboarding data normalization.
	- Views with role-based guards and ownership checks.
	- Signals for change tracking and email notifications.

- Project: `legal_portal`
	- Environment-aware settings via `.env`.
	- Database selection through `DATABASE_URL`.
	- Static/media configuration for local and production.

### Templates

- Server-rendered Django templates for landing, onboarding, dashboard, and case detail pages.

## Project Structure

```text
core/
	models.py
	forms.py
	views.py
	urls.py
	signals.py
	utils/email_notifications.py
legal_portal/
	settings.py
	urls.py
templates/
manage.py
requirements.txt
Procfile
render.yaml
```

## Quick Start (Local)

### 1. Clone and enter project

```powershell
git clone https://github.com/<your-username>/<your-repo>.git
cd Law_Firm
```

### 2. Create and activate virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Create `.env`

Create a `.env` file in the project root.

For quick local development (SQLite):

```env
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=
```

For PostgreSQL (local or cloud), add:

```env
DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/DB_NAME
DB_SSL_REQUIRE=False
```

### 5. Run migrations and start server

```powershell
python manage.py migrate
python manage.py runserver
```

### 6. Create an admin user

```powershell
python manage.py createsuperuser
```

## Environment Variables

Required / commonly used:

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `DATABASE_URL` (required in production)
- `DB_SSL_REQUIRE`

Optional email automation:

- `EMAIL_BACKEND`
- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `EMAIL_USE_TLS`
- `DEFAULT_FROM_EMAIL`
- `AUTOMATION_NOTIFICATION_EMAILS` (comma-separated)

## Render Deployment

### Build command

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

### Start command

```bash
gunicorn legal_portal.wsgi --log-file -
```

### Production env recommendations

- `DEBUG=False`
- `DATABASE_URL=<managed-postgres-url>`
- `DB_SSL_REQUIRE=True`
- `ALLOWED_HOSTS=<your-service>.onrender.com`
- `CSRF_TRUSTED_ORIGINS=https://<your-service>.onrender.com`

Run migrations after deploy:

```bash
python manage.py migrate --noinput
```

## Security and Data Notes

- Do not commit `.env` or secrets.
- Keep `DEBUG=False` in production.
- Configure strict `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`.
- `media/` is local in this setup; use object storage (S3-compatible) for persistent production media.

## Useful Commands

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

## Possible Resume Bullets

- Developed a role-based legal operations portal in Django with custom email authentication and profile onboarding flows for clients and advocates.
- Implemented secure case lifecycle management (cases, hearings, tasks, documents) with ownership-based access controls.
- Built automated PDF case report generation and model-change email notifications to improve reporting and operational transparency.
- Deployed a production-ready web app using Gunicorn, WhiteNoise, PostgreSQL, and Render with environment-driven configuration.
