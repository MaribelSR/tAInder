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
from django.db.models import Q


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        try:
            # Obtener el User personalizado basado en el email del usuario
            tainder_user = User.objects.get(email=user.email)
            # Devolver solo el usuario actual y perfiles de Ais.
            return Profile.objects.filter(Q(user=tainder_user) | Q(user__isnull=True))
        except User.DoesNotExist:
            # Si no existe el usuario, devuelve solo los perfiles de Ais.
            return Profile.objects.filter(user__isnull=True)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]


class TagCategoryViewSet(viewsets.ModelViewSet):
    queryset = TagCategory.objects.all()
    serializer_class = TagCategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Un usuario solo puede ver su propio usuario.
        return User.objects.filter(email=self.request.user.email)


class AiViewSet(viewsets.ModelViewSet):
    queryset = Ai.objects.all()
    serializer_class = AiSerializer
    permission_classes = [permissions.IsAuthenticated]


class MatchViewSet(viewsets.ModelViewSet):
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        try:
            tainder_user = User.objects.get(email=user.email)
            # Solo podra ver los matches donde el usuerio es el profile_a o profile_b.
            return Match.objects.filter(
                Q(profile_a__user=tainder_user) | Q(profile_b__user=tainder_user)
            )
        except User.DoesNotExist:
            # No se devuelve ningún match si el usuario no existe.
            return Match.objects.none()


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        try:
            tainder_user = User.objects.get(email=user.email)
            # Solo podra ver los mensajes cuando hay match y el usuario esta entre los perfiles.
            user_matches = Match.objects.filter(
                Q(profile_a__user=tainder_user) | Q(profile_b__user=tainder_user)
            )
            return Message.objects.filter(match__in=user_matches)
        except User.DoesNotExist:
            # No devuelve mensaje al no ser uno de los perfiles de match.
            return Message.objetcs.none()


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

    Posibilidad de añadirlo así:
        # Más eficiente con una sola query
    matches = Match.objects.filter(
        Q(profile_a=tainder_user.profile) | Q(profile_b=tainder_user.profile)
    )
    
    matches_as_string = [match.to_json() for match in matches]
    response = "[{}]".format(",".join(matches_as_string))
    return HttpResponse(response)
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
