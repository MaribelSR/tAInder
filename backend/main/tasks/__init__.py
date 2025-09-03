from main.models import Match, Message, Profile, Ai
import requests
import json
from datetime import datetime, timezone
from main.tasks.generate_profile import (
    generate_profile_and_tags,
)
from main.serializers import ProfileNestedSerializer
from rest_framework.renderers import JSONRenderer


def generate_profile(
    number=1, tags_sexuality=[], url="http://localhost:11434/api/generate"
):
    for i in range(number):
        profile, tags = generate_profile_and_tags(
            url=url, tags_sexuality=tags_sexuality
        )

        profileAsObject = Profile.objects.create(
            height=profile["height"],
            birthday=profile["birthday"],
            description=profile["description"],
        )
        for tag in tags:
            profileAsObject.tags.add(tag.id)

        Ai.objects.create(
            profile=profileAsObject,
            username=profile["username"],
            first_name=profile["first_name"],
            last_name=profile["last_name"],
        )


def generate_message_reply(url="http://localhost:11434/api/generate"):
    for match in Match.objects.filter(do_match=True):
        last_msg = (
            match.message_set.exclude(deleted=True).order_by("-published").first()
        )
        if not last_msg:
            continue
        # Skip Match that last Message is from Ai
        if last_msg.profile.ai_set.first():
            print("Skip {} because the last message its from Ai".format(match))
            continue

        ai_profile = match.ai_profile
        user_profile = match.user_profile

        # Llamada a la API de Ollama
        # TODO mejorar prompt
        serializer_ai = ProfileNestedSerializer(ai_profile)
        json_ai_profile = JSONRenderer().render(serializer_ai.data)
        serializer_user = ProfileNestedSerializer(user_profile)
        json_user_profile = JSONRenderer().render(serializer_user.data)

        prompt = """
                Interpretando el siguiente perfil; teniendo en cuenta los tags de personalidad a la hora de responder el mensaje (no incluir descripción ni tags en la respuesta): {ai_profile}
                Contesta al siguiente mensaje: {last_msg}
                Perteneciente al usuario: {user_profile}.
            """.format(
            ai_profile=json_ai_profile.decode("utf-8"),
            last_msg=last_msg.msg,
            user_profile=json_user_profile.decode("utf-8"),
        )
        if match.summary:
            prompt += "Resumen previo: {summary}\n".format(summary=match.summary)
        prompt += 'Tu respuesta debe ser un JSON con el siguiente formato: {"response": "Tu respuesta"}\n'
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
        ai_response = response.json()
        if "response" not in ai_response:
            print(ai_response)
            raise Exception("No se ha generado una respuesta del Ollama")
        msg = ai_response["response"]
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


def generate_match_summary(url="http://localhost:11434/api/generate"):
    for match in Match.objects.all():
        messages = (
            match.message_set.exclude(deleted=True)
            .exclude(summarized=True)
            .order_by("published")
        )
        if not messages:
            continue

        # Llamada a la API de Ollama
        prompt = 'Resume la conversación y tu respuesta debe seguir el siguiente formato: {{"summary": "Resumen"}}\n'

        if match.summary:
            prompt += "Resumen previo: {summary}\n".format(summary=match.summary)
        for msg in messages:
            if msg.profile.is_from_user():
                username = msg.profile.user_set.first().username
            elif msg.profile.is_from_ai():
                username = msg.profile.ai_set.first().username
            else:
                username = ""
            prompt += "{username}: {msg}\n".format(username=username, msg=msg.msg)

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
        r = response.json()
        if "response" not in r:
            print(r)
            raise Exception("No se ha generado un resumen del Ollama")
        summary = r["response"]
        summary = json.loads(summary)
        summary = summary["summary"]

        print(summary)
        match.summary = summary
        match.save()
        for msg in messages:
            msg.summarized = True
            msg.save()
