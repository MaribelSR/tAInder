import base64
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.db.models import Q


class HttpHeaderAuthBasicAuthentication(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        if request is None:
            return None
        for header in request.headers:
            if header.lower() != "authorization":
                continue
            auth_header = request.headers[header]
            auth_header = auth_header.removeprefix("Basic ")
            auth_header = base64.b64decode(auth_header).decode()
            username_or_email = auth_header.split(":", 1)[0]
            password = auth_header.split(":", 1)[1]

            user = User.objects.filter(
                    Q(username=username_or_email) | Q(email=username_or_email)
            ).first()
            if not user or not check_password(password, user.password):
                return None
            return user
