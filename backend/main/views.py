from main.models import Profile, Tag, TagCategory
from rest_framework import permissions, viewsets
from main.serializers import ProfileSerializer, TagSerializer, TagCategorySerializer


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
