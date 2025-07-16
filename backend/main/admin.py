from django.contrib import admin
from .models import Profile, Message, Ai, Match, Tag, TagCategory, User

admin.site.register(Profile)
admin.site.register(Message)
admin.site.register(Ai)
admin.site.register(Match)
admin.site.register(Tag)
admin.site.register(TagCategory)
admin.site.register(User)
