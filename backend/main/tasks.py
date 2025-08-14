from main.models import Match, Message
import requests
import json
from datetime import datetime, timezone


def generate_profile():
    pass


def generate_message_reply(url="http://localhost:11434/api/generate"):
    for match in Match.objects.filter(do_match=True):
        last_msg = match.message_set.exclude(deleted=True).order_by("-published")[0]
        # Skip Match that last Message is from Ai
        if last_msg.profile.ai_set.first():
            print("Skip {} because the last message its from Ai".format(match))
            continue

        ai_profile = match.ai_profile
        user_profile = match.user_profile

        # Llamada a la API de Ollama
        # TODO mejorar prompt
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
            url=url,
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
            raise Exception("No se ha generado una respuesta del Ollama")
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
