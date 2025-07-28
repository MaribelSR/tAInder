from django.http import HttpResponse
from django.shortcuts import render
from main.models import Profile


# Create your views here.
def view_profiles(request):
    profiles = Profile.objects.all()
    response = ""
    for profile in profiles:
        response += profile.first_name + " " + profile.last_name + "<br>"
    response = """
{
    "profiles": [
        {
            "first_name": "John",
            "last_name": "Doe",
        },
        {
           "first_name": "Jane",
           "last_name": "Smith",
        }
    ]
}
"""
    return HttpResponse(response)
