# AgriTech Platform - Installation Guide

This guide will walk you through the process of setting up the AgriTech platform for development, testing, and production deployment.

## Development Environment Setup

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/agritech.git
cd agritech
```

### Step 2: Create a Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the root directory:

```
DJANGO_SECRET_KEY=your_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Step 5: Set Up the Database

```bash
python manage.py migrate
```

### Step 6: Create a Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin user.

### Step 7: Run the Development Server

```bash
python manage.py runserver
```

The application will be available at http://127.0.0.1:8000/

## Loading Initial Data

AgriTech comes with sample data to help you get started quickly.

### Load Categories and Tags

```bash
python manage.py loaddata categories_tags.json
```

### Load Sample Content

```bash
python manage.py loaddata sample_content.json
```

## Testing

### Running Tests

```bash
python manage.py test
```

### Test Coverage

To check test coverage:

```bash
coverage run --source='.' manage.py test
coverage report
```

## Production Deployment

### Step 1: Configure Production Settings

Edit `agritech/settings.py` or create a separate production settings file:

```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Configure database for production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Static and media files configuration
STATIC_ROOT = '/var/www/yourdomain.com/static/'
MEDIA_ROOT = '/var/www/yourdomain.com/media/'
```

### Step 2: Set Up PostgreSQL Database

Install PostgreSQL:

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

Create a database and user:

```bash
sudo -u postgres psql

CREATE DATABASE your_db_name;
CREATE USER your_db_user WITH PASSWORD 'your_db_password';
ALTER ROLE your_db_user SET client_encoding TO 'utf8';
ALTER ROLE your_db_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE your_db_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_db_user;
\q
```

### Step 3: Set Up Gunicorn

Install Gunicorn:

```bash
pip install gunicorn
```

Create a systemd service file for Gunicorn:

```bash
sudo nano /etc/systemd/system/gunicorn_agritech.service
```

Add the following content:

```
[Unit]
Description=gunicorn daemon for AgriTech
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/agritech
ExecStart=/path/to/agritech/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/path/to/agritech/agritech.sock \
          agritech.wsgi:application

[Install]
WantedBy=multi-user.target
```

Start and enable the Gunicorn service:

```bash
sudo systemctl start gunicorn_agritech
sudo systemctl enable gunicorn_agritech
```

### Step 4: Configure Nginx

Install Nginx:

```bash
sudo apt install nginx
```

Create an Nginx server block:

```bash
sudo nano /etc/nginx/sites-available/agritech
```

Add the following content:

```
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /var/www/yourdomain.com;
    }

    location /media/ {
        root /var/www/yourdomain.com;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/path/to/agritech/agritech.sock;
    }
}
```

Enable the server block:

```bash
sudo ln -s /etc/nginx/sites-available/agritech /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### Step 5: Set Up SSL with Let's Encrypt

Install Certbot:

```bash
sudo apt install certbot python3-certbot-nginx
```

Obtain and install a certificate:

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Follow the prompts to complete the SSL configuration.

### Step 6: Final Steps

Collect static files:

```bash
python manage.py collectstatic
```

Apply migrations:

```bash
python manage.py migrate
```

Create a superuser if you haven't already:

```bash
python manage.py createsuperuser
```

## Updating the Application

To update the application to the latest version:

```bash
cd /path/to/agritech
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic
sudo systemctl restart gunicorn_agritech
```

## Backup and Restore

### Database Backup

```bash
pg_dump -U your_db_user -d your_db_name > backup_$(date +%Y-%m-%d).sql
```

### Database Restore

```bash
psql -U your_db_user -d your_db_name < backup_file.sql
```

### Media Files Backup

```bash
tar -czf media_backup_$(date +%Y-%m-%d).tar.gz /var/www/yourdomain.com/media
```

## Troubleshooting

### Common Issues

1. **Static files not loading**:
   - Check STATIC_ROOT and STATIC_URL settings
   - Ensure collectstatic has been run
   - Verify Nginx configuration

2. **Database connection errors**:
   - Check database credentials in settings.py
   - Ensure PostgreSQL service is running
   - Verify firewall settings

3. **500 Internal Server Error**:
   - Check Gunicorn and Nginx error logs
   - Verify correct permissions on files and directories
   - Check for syntax errors in code

### Log Locations

- Nginx access log: `/var/log/nginx/access.log`
- Nginx error log: `/var/log/nginx/error.log`
- Gunicorn log: System journal (`journalctl -u gunicorn_agritech`)
- Django log: Defined in settings.py, typically in the project root