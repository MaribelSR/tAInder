from django.core.management.base import BaseCommand
from main.models import Profile
import requests


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Hello, world!")

        """
        print(Profile.objects.all())
        maribel = Profile.objects.get(username="maribelSR")
        maribel.delete()
        print(Profile.objects.all())
         try:
            maribel = Profile.objects.create(
                username="maribelSR",
                first_name="Maribel",
                last_name="Salvador Rufo",
                height=173,
                birthday="1992-09-17",
                description="I'm a girl",
            )
        except Exception as e:
            print(e)
        """
        # Peticiones pag web
        # web = requests.get("https://www.google.com")
        # print(web.status_code)
        prompt = "Dime propuestas para hacer hoy"
        response = requests.post(
            url="http://localhost:11434/api/generate",
            json={"model": "gemma3:latest", "prompt": prompt, "stream": False},
        )
        aIresponse = response.json()
        msg = aIresponse["response"]
        print(msg)
