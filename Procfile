release: python manage.py migrate
web: gunicorn server.wsgi --bind 0.0.0.0:$PORT
