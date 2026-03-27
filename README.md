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
- PostgreSQL

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

## PostgreSQL Setup (Windows)

PostgreSQL is already connected for local development.

1. Create a DB user in pgAdmin (recommended)

- Open pgAdmin and expand your server.
- Open Login/Group Roles -> right click -> Create -> Login/Group Role.
- Name: lawfirm_user
- Set a password and enable Login.

2. Grant DB privileges

- Open Query Tool and run:

```sql
GRANT ALL PRIVILEGES ON DATABASE law_firm_db TO lawfirm_user;
```

3. Set local DATABASE_URL in .env

```env
DATABASE_URL=postgresql://lawfirm_user:YOUR_PASSWORD@localhost:5432/law_firm_db
```

4. Install dependencies (includes python-dotenv and psycopg2)

```powershell
pip install -r requirements.txt
```

5. Run migrations on PostgreSQL

```powershell
python manage.py migrate
```

6. Run server and verify

```powershell
python manage.py runserver
```

If the app starts successfully, Django is connected to PostgreSQL.

7. Confirm active database from Django shell (optional)

```powershell
python manage.py shell -c "from django.conf import settings; print(settings.DATABASES['default'])"
```

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

## Deploy to Render (Manual, No Blueprint)

Use this flow when you want a manual deploy and do not want to use Blueprint.

1. Push your latest code to GitHub

```powershell
git add .
git commit -m "Prepare manual Render deployment"
git push
```

2. Create a PostgreSQL database connection for production

- If Render asks for card for managed Postgres, create a free PostgreSQL database on Neon or Supabase.
- Copy the full connection string with sslmode=require.

3. Create a new Web Service in Render

- Render Dashboard -> New + -> Web Service.
- Connect your GitHub repository.
- Branch: main.
- Runtime: Python 3.
- Plan: Free (or your preferred plan).

4. Set build and start commands

- Build Command:

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

- Pre-Deploy Command:

```bash
python manage.py migrate --noinput
```

- Start Command:

```bash
gunicorn legal_portal.wsgi --log-file -
```

5. Add environment variables in Render

- SECRET_KEY = strong random value
- DEBUG = False
- ALLOWED_HOSTS = your-service-name.onrender.com
- CSRF_TRUSTED_ORIGINS = https://your-service-name.onrender.com
- DATABASE_URL = your production PostgreSQL connection string
- DB_SSL_REQUIRE = True
- EMAIL_BACKEND, EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_TLS, DEFAULT_FROM_EMAIL, AUTOMATION_NOTIFICATION_EMAILS (if you use email features)

6. Create and wait for deployment

- Click Create Web Service.
- Wait until status becomes Live.

7. Create admin user on Render

- Open your service -> Shell.
- Run:

```bash
python manage.py createsuperuser
```

8. Verify the deployment

- Open https://your-service-name.onrender.com
- Open https://your-service-name.onrender.com/admin
- Login with your superuser account.

9. Future updates

- Push to main branch.
- Render auto-deploys the latest commit.

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
