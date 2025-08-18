from django.core.management.base import BaseCommand, CommandError
from main.tasks import generate_profile


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
            generate_profile(number=number, url=url, tags_sexuality=tags_sexuality)
        except Exception as e:
            raise CommandError(e)
