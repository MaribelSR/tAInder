from django.db import models


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

    def to_json(self):
        return '{{"name": "{name}","category": "{category.name}"}}'.format(
            name=self.name, category=self.category
        )


class Profile(models.Model):
    username = models.CharField(max_length=150, unique=True, null=False)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    height = models.IntegerField()
    birthday = models.DateField(null=False)
    description = models.TextField(max_length=1024)
    last_access = models.DateTimeField(null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return "{username} ({last_name}, {first_name})".format(
            username=self.username, last_name=self.last_name, first_name=self.first_name
        )

    def to_json(self):
        return '{{"username": "{username}","first_name": "{first_name}","last_name": "{last_name}","height": {height},"birthday": "{birthday}","description": "{description}","last_access": "{last_access}","tags": [{tags}]}}'.format(
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            height=self.height,
            birthday=self.birthday,
            description=self.description,
            last_access=self.last_access,
            tags=", ".join([tag.to_json() for tag in self.tags.all()]),
        )


class User(models.Model):
    email = models.EmailField(max_length=254, unique=True, null=False)
    password = models.CharField(max_length=128, null=False)
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)


class Ai(models.Model):
    schedule = models.TextField()
    last_execution = models.DateTimeField(null=True)
    next_execution = models.DateTimeField(null=True)
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "AI"


class Match(models.Model):
    profile_a = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=False,
        related_name="matches_as_profile_a",
    )
    profile_b = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=False,
        related_name="matches_as_profile_b",
    )
    do_match_a_b = models.BooleanField()
    do_match_b_a = models.BooleanField()

    class Meta:
        verbose_name_plural = "Matches"


class Message(models.Model):
    msg = models.TextField()
    published = models.DateTimeField()
    deleted = models.BooleanField()
    replied_message = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=False)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, null=False)
