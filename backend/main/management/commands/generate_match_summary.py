from django.core.management.base import BaseCommand, CommandError
from main.tasks import generate_match_summary


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            generate_match_summary(options["url"])
        except Exception as e:
            raise CommandError(e)

    def add_arguments(self, parser):
        parser.add_argument(
            "--url",
            default="http://localhost:11434/api/generate",
            nargs="?",
            help="URL to generate message reply",
        )
