from django.core.management.base import BaseCommand, CommandError
from main.models import Profile, TagCategory, Tag
import requests
import json
import random
import sys


class Command(BaseCommand):
    def handle(self, *args, **options):
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
        prompt = """
                Genera un perfil para una aplicación para conocer personas 
                con los campos, username, first_name, last_name, height, birthday, 
                description, personality, schedule, next_execution.
                
                FORMATO DE RESPUESTA: Responde ÚNICAMENTE con un JSON válido con esta estructura exacta:
                {
                "username": "ejemplo_usuario123",
                "first_name": "Nombre",
                "last_name": "Apellido1 Apellido2",
                "height": 175,
                "birthday": "1990-05-15",
                "description": "Descripción en primera persona...",
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
        # TODO elegir 2 tags de categoría sexualidad.
        tagCategorySexuality = TagCategory.objects.get(name="Sexuality")
        sexualitiesAsObjects = random.sample(
            list(tagCategorySexuality.tag_set.all()), k=2
        )
        sexualitiesAsStrings = []
        for sexuality in sexualitiesAsObjects:
            sexualitiesAsStrings.append(sexuality.name)
        # sexualitiesAsStrings = [sexuality.name for sexuality in Tag.objects.filter(category__name="Sexuality").order_by("?")[:2]]
        prompt += "\nSexualidad: {}".format(",".join(sexualitiesAsStrings))

        # TODO elegir 3-5 tags de categoria hobby
        tagCategoryHobby = TagCategory.objects.get(name="Hobby")
        hobbiesAsObjects = random.sample(
            list(tagCategoryHobby.tag_set.all()), k=random.randint(3, 5)
        )
        hobbiesAsStrings = []
        for hobby in hobbiesAsObjects:
            hobbiesAsStrings.append(hobby.name)
        prompt += "\nHobbies: {}".format(",".join(hobbiesAsStrings))

        # TODO elegir 3-5 tags de categoria personalidad.
        tagCategoryPersonality = TagCategory.objects.get(name="Personality")
        personalitiesAsObjects = random.sample(
            list(tagCategoryPersonality.tag_set.all()), k=random.randint(3, 5)
        )
        personalitiesAsStrings = []
        for personality in personalitiesAsObjects:
            personalitiesAsStrings.append(personality.name)
        prompt += "\nPersonalidad: {}".format(",".join(personalitiesAsStrings))

        # TODO elegir 1-2 tags de categoria profesión.
        tagCategoryProfession = TagCategory.objects.get(name="Profession")
        professionsAsObjects = random.sample(
            list(tagCategoryProfession.tag_set.all()), k=random.randint(1, 2)
        )
        professionsAsStrings = []
        for profession in professionsAsObjects:
            professionsAsStrings.append(profession.name)
        prompt += "\nProfesión: {}".format(",".join(professionsAsStrings))

        # TODO elegir 3-5 tags de la categoria estilo de vida.
        tagCategoryLifeStyle = TagCategory.objects.get(name="Life Style")
        lifeStylesAsObjects = random.sample(
            list(tagCategoryLifeStyle.tag_set.all()), k=random.randint(3, 5)
        )
        lifeStylesAsStrings = []
        for lifeStyle in lifeStylesAsObjects:
            lifeStylesAsStrings.append(lifeStyle.name)
        prompt += "\nEstilo de vida: {}".format(",".join(lifeStylesAsStrings))

        prompt += "\n\nIntenta evitar los siguientes nombres:"
        for profile in Profile.objects.values("first_name").distinct():
            prompt += "\n-{}".format(profile["first_name"])

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
        print(msg)
        # Parse json to python dict
        profile = json.loads(msg)

        Profile.objects.create(
            username=profile["username"],
            first_name=profile["first_name"],
            last_name=profile["last_name"],
            height=profile["height"],
            birthday=profile["birthday"],
            description=profile["description"],
            # TODO asignar tags
            # tags=sexualitiesAsObjects
            # + hobbiesAsObjects
            # + personalitiesAsObjects
            # + professionsAsObjects
            # + lifeStylesAsObjects,
        )
