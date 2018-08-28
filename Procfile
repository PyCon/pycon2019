release: python manage.py migrate --noinput
web: gunicorn symposion.wsgi
worker: celery -A pycon worker --beat
