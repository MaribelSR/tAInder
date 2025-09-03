from django.core.management.base import BaseCommand, CommandError
from main.tasks import generate_message_reply
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            generate_message_reply(options["url"])
        except Exception as e:
            raise CommandError(e)

    def add_arguments(self, parser):
        parser.add_argument(
            "--url",
            default=settings.TAINDER_OLLAMA_URL,
            nargs="?",
            help="URL to generate message reply",
        )
