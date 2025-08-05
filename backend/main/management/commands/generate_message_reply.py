from django.core.management.base import BaseCommand, CommandError
import requests
from main.models import Match, Message
import json
from datetime import datetime, timezone


class Command(BaseCommand):
    def handle(self, *args, **options):
        for match in Match.objects.filter(do_match_a_b=True, do_match_b_a=True):
            try:
                last_msg = match.message_set.exclude(deleted=True).order_by(
                    "-published"
                )[0]
                # Skip Match that last Message is from Ai
                if last_msg.profile.ai_set.first():
                    print("Skip {} because the last message its from Ai".format(match))
                    continue
                # sacar perfil de la Ai
                ai_profile = None
                user_profile = None
                if match.profile_a.ai_set.first():
                    ai_profile = match.profile_a
                    user_profile = match.profile_b
                else:
                    ai_profile = match.profile_b
                    user_profile = match.profile_a

                # TODO Llamada a la API de Ollama
                prompt = """
                    Interpretando el siguiente perfil (no incluir descripción ni tags en la respuesta): {ai_profile}
                    Contesta al siguiente mensaje: {last_msg}
                    Perteneciente al usuario: {user_profile}.
                    Tu respuesta debe seguir el siguiente formato: {{"response": "Contestación"}}
                """.format(
                    ai_profile=ai_profile.to_json(),
                    last_msg=last_msg.msg,
                    user_profile=user_profile.to_json(),
                )
                print(prompt)
                response = requests.post(
                    url="http://localhost:11434/api/generate",
                    json={
                        "model": "gemma3:latest",
                        "prompt": prompt,
                        "stream": False,
                        "format": "json",
                    },
                )
                aIresponse = response.json()
                if "response" not in aIresponse:
                    print(aIresponse)
                    raise CommandError("No se ha generado una respuesta del Ollama")
                msg = aIresponse["response"]
                msg = json.loads(msg)
                msg = msg["response"]
                print(msg)

                Message.objects.create(
                    msg=msg,
                    published=datetime.now(timezone.utc),
                    deleted=False,
                    replied_message=last_msg,
                    profile=ai_profile,
                    match=match,
                )
            except Exception as e:
                print(e)
