from django.contrib import admin
from .models import Profile, Message, Ai, Match, Tag, TagCategory, User


class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        "username",
        "first_name",
        "last_name",
    ]
    ordering = ["username"]


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


class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "profile"]


class AiAdmin(admin.ModelAdmin):
    list_display = [
        "profile",
        "schedule",
        "last_execution",
        "next_execution",
    ]


class MessageInLine(admin.TabularInline):
    model = Message


class MatchAdmin(admin.ModelAdmin):
    list_display = [
        "profile_a",
        "profile_b",
        "do_match_a_b",
        "do_match_b_a",
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
    ]


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Ai, AiAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(TagCategory, TagCategoryAdmin)
admin.site.register(User, UserAdmin)
