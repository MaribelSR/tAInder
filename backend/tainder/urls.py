"""
URL configuration for tainder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from main.views import (
    ProfileViewSet,
    TagViewSet,
    TagCategoryViewSet,
    UserViewSet,
    AiViewSet,
    MatchViewSet,
    MessageViewSet,
    get_user_profile,
)

router = routers.DefaultRouter()
router.register(r"profiles", ProfileViewSet)
router.register(r"tags", TagViewSet)
router.register(r"tag-categories", TagCategoryViewSet)
router.register(r"users", UserViewSet)
router.register(r"aies", AiViewSet)
router.register(r"matches", MatchViewSet)
router.register(r"messages", MessageViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include(router.urls)),
    path("api/current_user/profile", get_user_profile),
]
