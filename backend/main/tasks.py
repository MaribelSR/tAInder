from main.models import Match, Message, Tag, TagCategory, Profile
import requests
import json
from datetime import datetime, timezone
import random


def generate_profile_prompt():
    """
    Genera el prompt para crear perfiles de usuarios AI.
    """
    return """
            Genera un perfil para una aplicación para conocer personas 
            con el siguiente formato:
            
            FORMATO DE RESPUESTA: Responde ÚNICAMENTE con un JSON válido con esta estructura exacta:
            {
            "username": "ejemplo_usuario123",
            "first_name": "Nombre",
            "last_name": "Apellido1 Apellido2",
            "height": 175,
            "birthday": "1990-05-15",
            "description": "Descripción en primera persona..."
            }

            Intrucciones específicas: 
            - El campo height es un número entero en centímetros(150-210).
            - Respóndeme solamente con un json.
            - El campo username tiene que ser único. Siguiendo estos patrones:
            "nombre_apellido_número", "aficiones_número", "nombreAfición", "apellido_número", 
            "númeroNombrenúmero".
            - En España en el campo last_name son dos apellidos y se guardará como texto plano.
            - El campo descripción debe ser lenguaje coloquial y cercano, en primera persona. Que transmita parte de su personalidad y sus gustos.
            - El perfil tiene que ser atrayante.
            - El perfil tiene que estar escrito en español.
            
        """


# DUDA: Cambio lo de opts por el parametro en si de tags_sexuality por tema de responsabilidad unica. Le he encontrado sentido.
# Al final comentaba que asi cada función recibe solo que necesita. No lo veo mal.
def generate_prompt_tags(tags_sexuality=None):
    # Genera un prompt para generar tags para el perfil.
    prompt = ""
    # Elige 2 tags de categoría sexualidad.
    tagCategorySexuality = TagCategory.objects.get(name="Sexuality")
    sexualitiesAsObjects = []
    if tags_sexuality is not None and len(tags_sexuality) > 0:
        sexualitiesAsObjects = Tag.objects.filter(
            name__in=tags_sexuality, category=tagCategorySexuality
        )
    else:
        tagMale = Tag.objects.get(name="male")
        tagFemale = Tag.objects.get(name="female")
        sexualitiesAsObjects = random.sample([tagMale, tagFemale], k=1)
        sexualitiesAsObjects += random.sample(
            list(tagCategorySexuality.tag_set.exclude(name__in=["male", "female"])),
            k=2,
        )

    sexualitiesAsStrings = []
    for sexuality in sexualitiesAsObjects:
        sexualitiesAsStrings.append(sexuality.name)
    # sexualitiesAsStrings = [sexuality.name for sexuality in Tag.objects.filter(category__name="Sexuality").order_by("?")[:2]]
    prompt += "\nSexualidad: {}".format(",".join(sexualitiesAsStrings))

    # Elige 3-5 tags de categoria hobby
    tagCategoryHobby = TagCategory.objects.get(name="Hobby")
    hobbiesAsObjects = random.sample(
        list(tagCategoryHobby.tag_set.all()), k=random.randint(3, 5)
    )
    hobbiesAsStrings = []
    for hobby in hobbiesAsObjects:
        hobbiesAsStrings.append(hobby.name)
    prompt += "\nHobbies: {}".format(",".join(hobbiesAsStrings))

    # Elige 3-5 tags de categoria personalidad.
    tagCategoryPersonality = TagCategory.objects.get(name="Personality")
    personalitiesAsObjects = random.sample(
        list(tagCategoryPersonality.tag_set.all()), k=random.randint(3, 5)
    )
    personalitiesAsStrings = []
    for personality in personalitiesAsObjects:
        personalitiesAsStrings.append(personality.name)
    prompt += "\nPersonalidad: {}".format(",".join(personalitiesAsStrings))

    # Elige 1-2 tags de categoria profesión.
    tagCategoryProfession = TagCategory.objects.get(name="Profession")
    professionsAsObjects = random.sample(
        list(tagCategoryProfession.tag_set.all()), k=random.randint(1, 2)
    )
    professionsAsStrings = []
    for profession in professionsAsObjects:
        professionsAsStrings.append(profession.name)
    prompt += "\nProfesión: {}".format(",".join(professionsAsStrings))

    # Elige 3-5 tags de la categoria estilo de vida.
    tagCategoryLifeStyle = TagCategory.objects.get(name="Life Style")
    lifeStylesAsObjects = random.sample(
        list(tagCategoryLifeStyle.tag_set.all()), k=random.randint(3, 5)
    )
    lifeStylesAsStrings = []
    for lifeStyle in lifeStylesAsObjects:
        lifeStylesAsStrings.append(lifeStyle.name)
    prompt += "\nEstilo de vida: {}".format(",".join(lifeStylesAsStrings))
    prompt += "\n"
    tags = (
        sexualitiesAsObjects
        + hobbiesAsObjects
        + personalitiesAsObjects
        + professionsAsObjects
        + lifeStylesAsObjects
    )
    return prompt, tags


def generate_prompt_avoid_first_names():
    # Evita que se genere nombres ya existentes.
    prompt = "\nIntenta evitar los siguientes nombres:"
    for profile in Profile.objects.values("first_name").distinct():
        prompt += "\n-{}".format(profile["first_name"])
    return prompt + "\n"


def generate_profile_and_tags(
    url="http://localhost:11434/api/generate", tags_sexuality=None
):
    # Genera los datos del perfil usando la IA.
    prompt = generate_profile_prompt()
    prompt_tags, tags = generate_prompt_tags(tags_sexuality)
    prompt += prompt_tags
    prompt += generate_prompt_avoid_first_names()
    print(prompt)

    # Llamada a la IA
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
    print(msg)
    # Parse json to python dict
    profile = json.loads(msg)
    return profile, tags


def generate_schedule_for_profile(profile, url="http://localhost:11434/api/generate"):
    prompt = """
            Genera una respuesta siguiendo el formato siguiente:
            {
                "schedule": {
                    "monday": [
                        {"start": "0:00", "end": "6:30", "description": "sleep"},
                        {"start": "6:30", "end": "7:30", "description": "wake-up and breakfast"},
                        {"start": "7:30", "end": "8:00", "description": "drive to work"},
                        ...
                        {"start": "21:30", "end": "22:00", "description": "dinner"},
                        {"start": "22:00", "end": "23:00", "description": "free and watch TV"},
                        {"start": "23:00", "end": "23:59", "description": "sleep"},
                    ],
                    ...
                }
            }
        """
    prompt += "\nBasandote en este perfil:\n"
    prompt += profile.to_json()
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
    print(msg)
    # Parse json to python dict
    schedule = json.loads(msg)
    return schedule


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
