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


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.filter(user__isnull=True)
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]


class TagCategoryViewSet(viewsets.ModelViewSet):
    queryset = TagCategory.objects.all()
    serializer_class = TagCategorySerializer
    permission_classes = [permissions.AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class AiViewSet(viewsets.ModelViewSet):
    queryset = Ai.objects.all()
    serializer_class = AiSerializer
    permission_classes = [permissions.AllowAny]


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [permissions.AllowAny]


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.AllowAny]
