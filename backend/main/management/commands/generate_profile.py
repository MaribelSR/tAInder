from django.core.management.base import BaseCommand, CommandError
from main.models import Profile, Ai
from main.tasks import (
    generate_profile_and_tags,
    generate_schedule_for_profile,
)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            "--num",
            default=1,
            type=int,
            nargs="?",
            help="Number of profiles to generate",
        )
        parser.add_argument(
            "--tags_sexuality", nargs="+", type=str, help="Tags for sexuality"
        )
        parser.add_argument(
            "--url",
            default="http://localhost:11434/api/generate",
            nargs="?",
            help="URL to generate profiles",
        )

    def handle(self, *args, **options):
        number = options["num"]
        url = options["url"]
        tags_sexuality = options.get("tags_sexuality")
        try:
            for i in range(number):
                profile, tags = generate_profile_and_tags(
                    url=url, tags_sexuality=tags_sexuality
                )

                profileAsObject = Profile.objects.create(
                    username=profile["username"],
                    first_name=profile["first_name"],
                    last_name=profile["last_name"],
                    height=profile["height"],
                    birthday=profile["birthday"],
                    description=profile["description"],
                )
                for tag in tags:
                    profileAsObject.tags.add(tag.id)

                schedule = generate_schedule_for_profile(
                    profile=profileAsObject, url=url
                )

                Ai.objects.create(
                    schedule=schedule,
                    profile=profileAsObject,
                )
        except Exception as e:
            raise CommandError(e)
