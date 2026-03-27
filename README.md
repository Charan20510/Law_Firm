# Law Firm Management Portal

A Django-based legal practice portal for managing clients, advocates, case records, onboarding data, and supporting documents.

## Features

- Client onboarding flow
- Advocate profile management
- Case detail tracking
- Role selection and dashboard views
- Document and media handling
- Django admin for operations
- Render-ready deployment configuration

## Tech Stack

- Python 3.11
- Django 5
- Gunicorn
- WhiteNoise
- PostgreSQL on Render (production)
- SQLite (local default)

## Project Structure

- core/: business logic, models, forms, views, urls
- legal_portal/: Django project settings and app entrypoints
- templates/: HTML templates
- media/: uploaded files (local)
- render.yaml: Render infrastructure blueprint
- Procfile: web process command

## Prerequisites

- Python 3.11+
- Git
- GitHub account
- Render account

## Local Setup

1. Clone repository

```powershell
git clone https://github.com/<your-username>/<your-repo>.git
cd Law_Firm
```

2. Create virtual environment and activate

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies

```powershell
pip install -r requirements.txt
```

4. Create local environment file

- Copy .env.example to .env
- Update values as needed

5. Run migrations and start server

```powershell
python manage.py migrate
python manage.py runserver
```

6. Create admin user

```powershell
python manage.py createsuperuser
```

## Environment Variables

Use these keys in your .env file (local) and Render Environment tab (production):

- SECRET_KEY
- DEBUG
- ALLOWED_HOSTS
- CSRF_TRUSTED_ORIGINS
- DATABASE_URL
- EMAIL_BACKEND
- EMAIL_HOST
- EMAIL_PORT
- EMAIL_HOST_USER
- EMAIL_HOST_PASSWORD
- EMAIL_USE_TLS
- DEFAULT_FROM_EMAIL
- AUTOMATION_NOTIFICATION_EMAILS

## Push to GitHub

If starting from this folder:

```powershell
git init -b main
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

If git is already initialized, just push:

```powershell
git push -u origin main
```

## Deploy to Render

This project already includes render.yaml and Procfile.

1. Push code to GitHub.
2. In Render, click New + and choose Blueprint.
3. Connect your GitHub repository.
4. Render will detect render.yaml and create:
   - web service
   - PostgreSQL database
5. Wait for build and deployment.
6. Open the web service Shell and create admin user:

```bash
python manage.py createsuperuser
```

## Static and Media Notes

- Static files are collected using WhiteNoise.
- media/ is ignored in git and is local by default.
- For production media persistence, use an external storage provider (for example S3-compatible storage).

## Useful Commands

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
python manage.py collectstatic --noinput
```

## Security Notes

- Never commit .env
- Keep DEBUG=False in production
- Set valid ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS in production

## License

For private/internal use unless you add a license file.
