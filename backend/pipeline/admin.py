from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "def_name",
        "status",
        "created_at",
        "locked_at",
        "locked_by",
        "retries",
        "unlocked_at",
    ]


admin.site.register(Task, TaskAdmin)
