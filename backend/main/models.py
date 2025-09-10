from django.db import models
from pipeline.models import Task
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser


class TagCategory(models.Model):
    name = models.CharField(max_length=64, unique=True, null=False)

    class Meta:
        verbose_name_plural = "Tag Categories"

    def __str__(self):
        return self.name


def get_tag_category_id_default():
    """
    default_category_as_slices = TagCategory.objects.filter(id=1)
    if len(default_category_as_slices) == 0:
        default_category = TagCategory.objects.create(name="Hidden", id=1)
        default_category_as_slices.append(default_category)
    return default_category_as_slices[0]
    """
    default_category, _ = TagCategory.objects.get_or_create(name="Hidden", id=1)
    return default_category.id


class Tag(models.Model):
    name = models.CharField(max_length=64, unique=False, null=False)
    category = models.ForeignKey(
        TagCategory, on_delete=models.CASCADE, default=get_tag_category_id_default
    )

    class Meta:
        unique_together = [
            ["name", "category"],
        ]

    def __str__(self):
        return "{category.name}: {name}".format(name=self.name, category=self.category)


class Profile(models.Model):
    height = models.IntegerField()
    birthday = models.DateField(null=False)
    description = models.TextField(max_length=1024)
    tags = models.ManyToManyField(Tag)

    def is_from_user(self):
        return hasattr(self, "user")

    def is_from_ai(self):
        return hasattr(self, "ai")

    def __str__(self):
        if self.is_from_user():
            return "{username} ({last_name}, {first_name})".format(
                username=self.user.username,
                last_name=self.user.last_name,
                first_name=self.user.first_name,
            )
        elif self.is_from_ai():
            return "{username} ({last_name}, {first_name})".format(
                username=self.ai.username,
                last_name=self.ai.last_name,
                first_name=self.ai.first_name,
            )
        else:
            return str(self.id)


class User(AbstractUser):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return "{username} ({last_name}, {first_name})".format(
            username=self.username,
            last_name=self.last_name,
            first_name=self.first_name,
        )


class Ai(models.Model):
    username = models.CharField(
        max_length=150,
        unique=False,
        default="",
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name = "AI"


class Match(models.Model):
    ai_profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=False,
        related_name="matches_as_ai_profile",
    )
    user_profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=False,
        related_name="matches_as_user_profile",
    )
    do_match = models.BooleanField(default=False)
    summary = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Matches"

    def __str__(self):
        return "Match: {ai_profile} - {user_profile}".format(
            ai_profile=self.ai_profile, user_profile=self.user_profile
        )

    def last_message(self):
        return self.message_set.order_by("published").last()


class Message(models.Model):
    msg = models.TextField()
    published = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
    replied_message = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=False)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, null=False)
    summarized = models.BooleanField(default=False)

    def __str__(self):
        return "{profile} - {msg}".format(profile=self.profile, msg=self.msg)


@receiver(post_save, sender=Message)
def message_post_save(sender, instance, created, raw, using, update_fields, **kwargs):
    if created:
        Task.objects.create(def_name="main.tasks.generate_match_summary")

    # Cuando instancia de Message haya sido creada por un usuario (no por AI):
    if created and instance.profile.is_from_user():
        # Crea tarea que ejecute generate_message_reply
        Task.objects.create(def_name="main.tasks.generate_message_reply")
