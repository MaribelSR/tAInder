import json
import random
import requests
from main.models import Tag, TagCategory, Ai
from django.conf import settings


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


def generate_prompt_tags(tags_sexuality=[]):
    # Genera un prompt para generar tags para el perfil.
    prompt = ""
    # Elige 2 tags de categoría sexualidad.
    tagCategorySexuality = TagCategory.objects.get(name="Sexuality")
    sexualitiesAsObjects = []
    if len(tags_sexuality) > 0:
        sexualitiesAsObjects = list(
            Tag.objects.filter(name__in=tags_sexuality, category=tagCategorySexuality)
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
    for ai in Ai.objects.values("first_name").distinct():
        prompt += "\n-{}".format(ai["first_name"])
    return prompt + "\n"


def generate_profile_and_tags(url=settings.TAINDER_OLLAMA_URL, tags_sexuality=[]):
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
            "model": settings.TAINDER_OLLAMA_MODEL,
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
