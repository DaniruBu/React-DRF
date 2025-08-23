pip install --root-user-action=ignore --no-cache-dir -r requirements.txt && \
python manage.py makemigrations && \
python manage.py migrate && \
python manage.py runserver 0.0.0.0:8000