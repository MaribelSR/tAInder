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
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response


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

    @action(detail=False, methods=["get"], name="Next AI Profile without Match")
    def next_ai_profile_without_match(self, request):
        tainder_user = User.objects.get(email=request.user.email)
        ai_profiles_id_already_matched = Match.objects.filter(
            user_profile=tainder_user.profile
        ).values("ai_profile")
        ai_profile = (
            Profile.objects.filter(ai__isnull=False)
            .exclude(id__in=ai_profiles_id_already_matched)
            .order_by("?")
            .first()
        )
        serializer = self.get_serializer(ai_profile)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def current(self, request):
        tainder_user = User.objects.get(email=request.user.email)
        serializer = self.get_serializer(tainder_user.profile)
        return Response(serializer.data)


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
    filterset_fields = ["email"]

    def get_queryset(self):
        # Un usuario solo puede ver su propio usuario.
        return User.objects.filter(email=self.request.user.email)

    @action(detail=False, methods=["get"], name="Current User")
    def current(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response(status=401)
        try:
            tainder_user = User.objects.get(email=user.email)
            serializer = self.get_serializer(tainder_user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(status=404)


class AiViewSet(viewsets.ModelViewSet):
    queryset = Ai.objects.all()
    serializer_class = AiSerializer
    permission_classes = [permissions.IsAuthenticated]


class MatchViewSet(viewsets.ModelViewSet):
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["do_match", "ai_profile", "user_profile"]

    def get_queryset(self):
        user = self.request.user
        try:
            tainder_user = User.objects.get(email=user.email)
            # Solo podra ver los matches donde el usuerio es el profile_a o profile_b.
            return Match.objects.filter(
                Q(ai_profile__user=tainder_user) | Q(user_profile__user=tainder_user)
            )
        except User.DoesNotExist:
            # No se devuelve ningún match si el usuario no existe.
            return Match.objects.none()

    @action(detail=True, methods=["get"], name="Last message")
    def last_message(self, request, pk=None):
        match = self.get_object()
        last_message = match.last_message()
        if last_message is None:
            return Response(status=404)
        serializer = MessageSerializer(last_message)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["match"]

    def create(self, request, *args, **kwargs):
        tainder_user = User.objects.get(email=request.user.email)
        request.data["profile"] = tainder_user.profile.id
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        try:
            tainder_user = User.objects.get(email=user.email)
            # Solo podra ver los mensajes cuando hay match y el usuario esta entre los perfiles.
            user_matches = Match.objects.filter(
                Q(ai_profile__user=tainder_user) | Q(user_profile__user=tainder_user)
            )
            return Message.objects.filter(match__in=user_matches)
        except User.DoesNotExist:
            # No devuelve mensaje al no ser uno de los perfiles de match.
            return Message.objetcs.none()
