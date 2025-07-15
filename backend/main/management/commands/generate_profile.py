from django.core.management.base import BaseCommand, CommandError
from main.models import Profile
import requests
import json
import random
import sys


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
        prompt = """
                Genera un perfil para una aplicación para conocer personas 
                con los campos, username, first_name, last_name, height, birthday, 
                description, personality, schedule, next_execution, tags (siguiendo la lista de tags).
                
                FORMATO DE RESPUESTA: Responde ÚNICAMENTE con un JSON válido con esta estructura exacta:
                {
                "username": "ejemplo_usuario123",
                "first_name": "Nombre",
                "last_name": "Apellido1 Apellido2",
                "height": 175,
                "birthday": "1990-05-15",
                "description": "Descripción en primera persona...",
                "tags": ["tag1", "tag2", "tag3"]
                }

                Intrucciones específicas: 
                - El campo height es un número entero en centímetros(150-210).
                - Respóndeme solamente con un json.
                - El campo username tiene que ser único. Siguiendo estos patrones:
                "nombre_apellido_número", "aficiones_número", "nombreAfición", "apellido_número", 
                "númeroNombrenúmero".
                - En España en el campo last_name son dos apellidos y se guardará como texto plano.
                - El campo descripción debe ser lenguaje coloquial y cercano, en primera persona. Que transmita parte de su personalidad y sus gustos.
                - El perfil tiene que ser atrayante para una persona de nacionalidad española y residente en España.
                - El perfil debe de ser equilibrado, comprobando la lista de 100 personas de la base de 
                datos y haciendo que haya tanto hombres como mujeres de forma equitativa, cada uno únicos.
                - El campo tags debe ser una lista de strings. 

                TAGS OBLIGATORIOS QUE PUEDEN INCLUIR DE FORMA ALEATORIA (HOMBRE/MUJER/OTROS): 
                - Personalidad: "extrovertido", "introvertido", "tranquilo", "nervioso", "impulsivo", "reflexivo",
                "agresivo", "sociable", "solitario", "creativo", "realista", "analítico", "pesimista", "optimista",
                "narcicista", "organizado", "espontáneo", "romántico", "independiente", "ambicioso", "conformista",
                "responsable", "pacífico", "dependiente", "empático", "sensible", "inteligente", "disciplinado", "compasivo",
                "servicial", "preocupado", "inestable", "ansioso", "irritable", "cooperativo", "asertivo", "enérgico", 
                "confiable", "persistente", "dócil", "serio", "aventurero", "apasionado", "maduro", "leal, "ileal", 
                "deshonesto", "honesto", "metódico", "caótico", "impredecible", "predecible", "reservado", 
                "impaciente", "paciente", "mentiroso", "directo", "sincero", "competente", "incompetente", "comprensivo", 
                "prudente", "crítico", "comprometido", "manipulador", "animalista". 

                - Hobbies: "leer", "escribir", "ver series", "ver películar", "cinéfilo", "pintor", "dibujante", "cerámica", "fútbol", "baloncesto"
                "deportes", "correr", "nadar", "bailar", "tenis", "golf", "padel", "crossfit", "gimnasio", "pilates", "yoga", 
                "crear contenido", "diseñar", "decorar", "gastronomía", "ajedrez", "coleccionismo", "cocina", "repostería", 
                "viajar", "artes marciales", "senderismo", "acampada", "pesca", "jardinería", "ciclismo", "surf", "deportes acuáticos", 
                "patinaje", "esquí", "béisbol", "hockey", "rugby", "escuchar música", "música", "cosplay", "teatro", "animes",
                "carpintería", "motos", "mecánica", "coches", "programación", "meditar", "escribir blogs", "aprender idiomas", 
                "ir de compras", "tocar instrumentos musicales", "cantar", "danza", "maquillaje", "conocer lugares nuevos", "visitar museos".

                - Profesión: "médico", "enfermero", "farmacéutico", "fisioterapeuta", "dentista", "veterinario", "psicólogo", "psiquiatra", 
                "otras ramas de ciencias", "abogado", "jurista", "procurador", "juez", "notario", "ingeniero", "informático", "maestro", "carpintero",
                "albañil", "fontanero", "cerrajero", "pintor", "mecánico", "sastre", "panadero", "carnicero", "cocinero", "joyero", "alfarero", "tejedor",
                "vidriero", "científico", "biólogo", "químico", "estadístico", "analista de datos", "programador web", "diseñador gráfico", "diseñador", 
                "community manager", "influencer", "creador de contenido digital", "arquitecto", "ingeniero industrial", "trabajador social", "educador social", 
                "sociólogo", "economista", "administrador", "empresario", "periodista", "filólogo", "traductor", "comercial", "ventas", "camarero", 
                "guía turístico", "recepcionista", "guardia", "bailarin", "policia", "militar", "guardia civil", "estudiante", "sin empleo", "piloto", "chófer", 
                "camionero", "cirujano", "astrónomo", "autónomo", "modelo", "azafato", "actor", "actriz", "músico", "otros". 

                - Orientación sexual/identidad sexual/sexualidad: "heterosexual", "homosexual", "bisexual", "asexual", "androginosexual", "antrosexual", "bicurioso", "demisexuales",
                "poliamorosos", "polisexual", "sapiosexual", "trans", "género binario", "no binario", "queer", "agénero", "bigénero", "género fluido", 
                "cisgénero", "intersexual", "transgénero", "transexual", "otros". 

                - Estilo de vida: "urbano", "rural", "madrugador", "noctámbulo", "social", "hogareño", "minimalista", "bohemio", "clásico",
                "moderno", "eco-friendly", "foodie", "viajero", "casero", "familiar", "saludable", "hábitos saludables", "fiestero", "mochilero".

                Los tags deben reflejarse en la descripción y personalidad del perfil, siguiendo los patrones mencionados.
                Incluye esos tags en el campo "tags" del Json. 
            
                - El perfil generado debe ser diferente, sin coincidencias, únicos, 
                y teniendo nombre y apellidos diferentes, a los siguientes: 
                """
        for profile in Profile.objects.all()[:101]:
            prompt += "\n-username: {}, first_name: {}, last_name: {}".format(
                profile.username,
                profile.first_name,
                profile.last_name,
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
        )
        
