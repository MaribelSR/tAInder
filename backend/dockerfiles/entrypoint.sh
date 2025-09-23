#!/usr/bin/env sh
set -ex

python manage.py migrate

python manage.py shell <<EOF
import secrets
from datetime import datetime
from main.models import User, Profile

if User.objects.all().count() == 0:
    pwd = secrets.token_urlsafe(16)
    p = Profile.objects.create(height=180, birthday=datetime.now())
    User.objects.create_superuser('admin', 'admin@localhost', pwd, profile=p, first_name="Administrador", last_name="Super")
    print(f'admin pwd: {pwd}')
EOF

exec python manage.py runserver 0.0.0.0:8000