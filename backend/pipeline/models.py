from django.db import models


class Task(models.Model):
    class Status(models.TextChoices):
        QUEUED = "queued", "Queued"
        PROCESSING = "processing", "Processing"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    def_name = models.CharField(max_length=1024, null=False)
    def_kwargs = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status, default=Status.QUEUED)
    created_at = models.DateTimeField(auto_now_add=True)
    locked_at = models.DateTimeField(null=True, blank=True)
    unlocked_at = models.DateTimeField(null=True, blank=True)
    locked_by = models.CharField(max_length=1024, null=True, blank=True)
    retries = models.IntegerField(default=0)
