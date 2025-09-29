from django.contrib import admin
from .models import Profile, Message, Ai, Match, Tag, TagCategory, User
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _
from django.http.response import HttpResponse


class ProfileAdmin(admin.ModelAdmin):
    change_list_template = "admin/profiles/change_list.html"

    def generate_profile(self, a):
        return HttpResponse(content="hola")

    def get_urls(self):
        from django.urls import path

        urls = super().get_urls()
        urls.insert(
            0,
            path(
                route="generate_profile/",
                view=self.generate_profile,
                name="generate_profile",
            ),
        )
        return urls


class TagAdmin(admin.ModelAdmin):
    list_display = [
        "category",
        "name",
    ]
    ordering = ["category", "name"]


class TagInline(admin.TabularInline):
    model = Tag


class TagCategoryAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]
    ordering = ["name"]
    inlines = [TagInline]


class UserAdmin(DjangoUserAdmin):
    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "profile",
        "is_staff",
    ]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "email", "profile")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "usable_password",
                    "password1",
                    "password2",
                    "profile",
                ),
            },
        ),
    )


class AiAdmin(admin.ModelAdmin):
    list_display = [
        "username",
        "first_name",
        "last_name",
        "profile",
    ]


class MessageInLine(admin.TabularInline):
    model = Message


class MatchAdmin(admin.ModelAdmin):
    list_display = [
        "ai_profile",
        "user_profile",
        "do_match",
        "summary",
    ]
    inlines = [MessageInLine]


class MessageAdmin(admin.ModelAdmin):
    list_display = [
        "msg",
        "published",
        "deleted",
        "replied_message",
        "profile",
        "match",
        "summarized",
    ]


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Ai, AiAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(TagCategory, TagCategoryAdmin)
admin.site.register(User, UserAdmin)
