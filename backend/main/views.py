from django.http import HttpResponse
from django.shortcuts import render
from main.models import Profile
import json


def view_ai_profiles(request):
    """
    Returns HttpResponse with all AI's profiles as Json.
    """
    """
    Crear diccionario con el siguiente formato:
    {"profiles":
    [
        {"first_name": "john","last_name": "doe"},
        {"first_name": "jane","last_name": "smith"},
    ]
    }
    """
    profiles = Profile.objects.filter(user__isnull=True)
    result = {
        "profiles": [],
    }
    for profile in profiles:
        result["profiles"].append(
            {
                "first_name": profile.first_name,
                "last_name": profile.last_name,
            }
        )

    # Convert dict to Json as str.
    response = json.dumps(result)

    return HttpResponse(response)
