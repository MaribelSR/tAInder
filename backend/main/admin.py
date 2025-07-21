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


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Message)
admin.site.register(Ai)
admin.site.register(Match)
admin.site.register(Tag, TagAdmin)
admin.site.register(TagCategory, TagCategoryAdmin)
admin.site.register(User)
