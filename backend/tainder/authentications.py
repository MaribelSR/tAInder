import base64
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import authenticate


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
            username = auth_header.split(":", 1)[0]
            password = auth_header.split(":", 1)[1]
            user = authenticate(username=username, password=password)
            return user
        return None
