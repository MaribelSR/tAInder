from django.core.management.base import BaseCommand, CommandError
from main.models import Profile, TagCategory, Tag, Ai
import requests
import json
import random
import sys


class Command(BaseCommand):
    def generate_prompt(self):
        """
        "schedule": {
                "monday": [
                    {"start": "0:00", "end": "6:30", "description": "sleep"},
                    {"start": "6:30", "end": "7:30", "description": "wake-up and breakfast"},
                    {"start": "7:30", "end": "8:00", "description": "drive to work"},
                    {"start": "8:00", "end": "14:00", "description": "work"},
                    {"start": "14:00", "end": "15:00", "description": "lunch"},
                    {"start": "15:00", "end": "18:00", "description": "free"}
                    {"start": "18:00", "end": "20:00", "description": "gym"},
                    {"start": "20:00", "end": "21:30", "description": "drive to home"},
                    {"start": "21:30", "end": "22:00", "description": "dinner"},
                    {"start": "22:00", "end": "23:00", "description": "free and watch TV"},
                    {"start": "23:00", "end": "23:59", "description": "sleep"},
                ],
                "tuesday": [
                    {"start": "0:00", "end": "6:30", "description": "sleep"},
                    {"start": "6:30", "end": "7:30", "description": "wake-up and breakfast"},
                    {"start": "7:30", "end": "8:00", "description": "drive to work"},
                    {"start": "8:00", "end": "14:00", "description": "work"},
                    ...
                ],
                ...
            }
            - El campo schedule estará basado en los tags, y debe de corresponder al perfil imaginado.
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

    def generate_profile_and_tags(self, options):
        # Peticiones pag web
        # web = requests.get("https://www.google.com")
        # print(web.status_code)

        prompt = self.generate_prompt()
        prompt_tags, tags = self.generate_prompt_tags(opts=options)
        prompt += prompt_tags
        prompt += self.generate_prompt_avoid_first_names()
        print(prompt)
        # TODO url options
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
        return profile, tags

    def generate_prompt_tags(self, opts):
        prompt = ""
        # TODO elegir 2 tags de categoría sexualidad.
        tagCategorySexuality = TagCategory.objects.get(name="Sexuality")
        sexualitiesAsObjects = []
        if opts["tags_sexuality"] is not None and len(opts["tags_sexuality"]) > 0:
            sexualitiesAsObjects = Tag.objects.filter(
                name__in=opts["tags_sexuality"], category=tagCategorySexuality
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
        prompt += "\n"
        tags = (
            sexualitiesAsObjects
            + hobbiesAsObjects
            + personalitiesAsObjects
            + professionsAsObjects
            + lifeStylesAsObjects
        )
        return prompt, tags

    def generate_prompt_avoid_first_names(self):
        prompt = "\nIntenta evitar los siguientes nombres:"
        for profile in Profile.objects.values("first_name").distinct():
            prompt += "\n-{}".format(profile["first_name"])
        return prompt + "\n"

    def add_arguments(self, parser):
        parser.add_argument(
            "--num",
            default=1,
            type=int,
            help="Number of profiles to generate",
        )
        parser.add_argument(
            "--tags_sexuality", nargs="+", type=str, help="Tags for sexuality"
        )

    def handle(self, *args, **options):
        number = options["num"]
        for i in range(number):
            profile, tags = self.generate_profile_and_tags(options=options)

            profileAsObject = Profile.objects.create(
                username=profile["username"],
                first_name=profile["first_name"],
                last_name=profile["last_name"],
                height=profile["height"],
                birthday=profile["birthday"],
                description=profile["description"],
            )
            for tag in tags:
                profileAsObject.tags.add(tag.id)

            # Ai.objects.create(
            #     schedule=profile["schedule"],
            #     profile=profileAsObject,
            # )
