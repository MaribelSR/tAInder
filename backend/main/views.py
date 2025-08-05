import base64
import json
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
from django.views.decorators.csrf import csrf_exempt


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
    user = authenticate(request)
    if user is None or not user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    try:
        tainder_user = User.objects.get(email=user.email)
        return HttpResponse(tainder_user.profile.to_json())
    except User.DoesNotExist:
        return HttpResponse("Unauthorized", status=401)


def get_match_user(request):
    user = authenticate(request)
    if user is None or not user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    try:
        tainder_user = User.objects.get(email=user.email)
    except User.DoesNotExist:
        return HttpResponse("Unauthorized", status=401)
    matches_user_a = Match.objects.filter(profile_a=tainder_user.profile)
    matches_user_b = Match.objects.filter(profile_b=tainder_user.profile)
    """
    matches = Match.objects.filter(profile_a=tainder_user.profile) | Match.objects.filter(profile_b=tainder_user.profile)
    """
    matches = []
    for match in matches_user_a:
        matches.append(match)
    for match in matches_user_b:
        matches.append(match)
    matches_as_string = []
    for match in matches:
        matches_as_string.append(match.to_json())
    all_matches_as_single_string = ",".join(matches_as_string)
    # response = "[{}]".format(",".join([match.to_json() for match in matches]))
    response = "[{}]".format(all_matches_as_single_string)
    return HttpResponse(response)


@csrf_exempt
def get_profile_by_user_email(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError as e:
        return HttpResponse(status=400)

    if "email" not in data or "password" not in data:
        return HttpResponse(status=400)
    email = data["email"]
    password = data["password"]

    try:
        user = User.objects.get(email=email, password=password)
    except User.DoesNotExist as e:
        return HttpResponse(status=404)

    return HttpResponse(user.profile.to_json())
