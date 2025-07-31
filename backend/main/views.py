import base64
import pprint
from main.models import Profile, Tag, TagCategory, User, Ai, Match, Message
from rest_framework import permissions, viewsets
from main.serializers import (
    ProfileSerializer,
    TagSerializer,
    TagCategorySerializer,
    UserSerializer,
    AiSerializer,
    MatchSerializer,
    MessageSerializer,
)
from django.http import HttpResponse
from django.contrib.auth import authenticate


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.filter(user__isnull=True)
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]


class TagCategoryViewSet(viewsets.ModelViewSet):
    queryset = TagCategory.objects.all()
    serializer_class = TagCategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class AiViewSet(viewsets.ModelViewSet):
    queryset = Ai.objects.all()
    serializer_class = AiSerializer
    permission_classes = [permissions.IsAuthenticated]


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAuthenticated]


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]


def get_user_profile(request):
    print(request.headers)
    for header in request.headers:
        if header.lower() != "authorization":
            continue
        auth_header = request.headers[header]
        auth_header = auth_header.removeprefix("Basic ")
        auth_header = base64.b64decode(auth_header).decode()
        username = auth_header.split(":")[0]
        password = auth_header.split(":")[1]
        user = authenticate(username=username, password=password)
        if user is not None:
            request.user = user
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)

    user = User.objects.get(email=request.user.email)
    return HttpResponse(user.profile.to_json())
