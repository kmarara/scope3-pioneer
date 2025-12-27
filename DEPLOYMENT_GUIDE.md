# 🚀 Production Deployment Guide

## Quick Start for Companies

### Option 1: Self-Hosted Deployment (Recommended)

#### Prerequisites
- Ubuntu 20.04+ or similar Linux server
- PostgreSQL 12+
- Python 3.10+
- Nginx (web server)
- Gunicorn (WSGI server)
- Domain name (optional but recommended)

#### Step 1: Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3-pip python3-venv python3-dev postgresql postgresql-contrib nginx git -y

# Install PostgreSQL
sudo -u postgres psql
CREATE DATABASE scope3_tracker;
CREATE USER scope3_user WITH PASSWORD 'your-secure-password';
GRANT ALL PRIVILEGES ON DATABASE scope3_tracker TO scope3_user;
\q
```

#### Step 2: Deploy Application

```bash
# Clone repository
cd /var/www
sudo git clone <your-repo-url> scope3_tracker
cd scope3_tracker

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn psycopg2-binary

# Set environment variables
cp .env.example .env
nano .env  # Edit with your production values
```

#### Step 3: Configure Environment Variables

Edit `.env` file:
```bash
SECRET_KEY=your-very-secure-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=postgresql://scope3_user:password@localhost:5432/scope3_tracker

# Email (for password resets)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

#### Step 4: Database Setup

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

#### Step 5: Configure Gunicorn

Create `/etc/systemd/system/scope3-tracker.service`:

```ini
[Unit]
Description=Scope 3 Tracker Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/scope3_tracker
Environment="PATH=/var/www/scope3_tracker/venv/bin"
ExecStart=/var/www/scope3_tracker/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/var/www/scope3_tracker/scope3_tracker.sock \
    scope3_tracker.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl start scope3-tracker
sudo systemctl enable scope3-tracker
```

#### Step 6: Configure Nginx

Create `/etc/nginx/sites-available/scope3_tracker`:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/scope3_tracker/scope3_tracker.sock;
    }

    location /static/ {
        alias /var/www/scope3_tracker/staticfiles/;
    }

    location /media/ {
        alias /var/www/scope3_tracker/media/;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/scope3_tracker /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Step 7: SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

---

### Option 2: Cloud Deployment (Heroku/Railway/Render)

#### Heroku Deployment

1. **Install Heroku CLI**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

2. **Login and Create App**
```bash
heroku login
heroku create scope3-tracker
```

3. **Set Environment Variables**
```bash
heroku config:set SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=scope3-tracker.herokuapp.com
```

4. **Add PostgreSQL**
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

5. **Deploy**
```bash
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

---

### Option 3: Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "scope3_tracker.wsgi:application", "--bind", "0.0.0.0:8000"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  db:
    image: postgres:14
    environment:
      POSTGRES_DB: scope3_tracker
      POSTGRES_USER: scope3_user
      POSTGRES_PASSWORD: your-password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    command: gunicorn scope3_tracker.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql://scope3_user:your-password@db:5432/scope3_tracker

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

```bash
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

---

## Production Checklist

### Security
- [ ] Change SECRET_KEY to random value
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Enable HTTPS/SSL
- [ ] Set secure cookie flags
- [ ] Configure CORS properly
- [ ] Set up firewall rules
- [ ] Enable rate limiting

### Database
- [ ] Migrate to PostgreSQL
- [ ] Set up database backups
- [ ] Configure connection pooling
- [ ] Set up read replicas (if needed)

### Monitoring
- [ ] Set up error logging
- [ ] Configure log rotation
- [ ] Set up uptime monitoring
- [ ] Configure alerts

### Performance
- [ ] Enable static file compression
- [ ] Set up CDN for static files
- [ ] Configure caching (Redis)
- [ ] Optimize database queries
- [ ] Set up load balancing (if needed)

---

## Post-Deployment

1. **Create First Tenant/Organization**
   - Go to `/accounts/register/`
   - Register your company
   - You'll be automatically logged in

2. **Configure Features**
   - Add suppliers
   - Connect IoT devices (if applicable)
   - Set up API keys for integrations
   - Create scenarios for planning

3. **User Management**
   - Invite team members via Admin panel
   - Assign roles (Owner, Admin, Member, Viewer)
   - Create API keys for programmatic access

---

## Maintenance

### Regular Tasks
- Database backups (daily)
- Update dependencies (monthly)
- Security patches (as needed)
- Monitor logs for errors
- Review and optimize performance

### Updates
```bash
# Pull latest code
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Update dependencies
pip install -r requirements.txt --upgrade

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart services
sudo systemctl restart scope3-tracker
```

---

**Need Help?** Check the documentation or contact support.

