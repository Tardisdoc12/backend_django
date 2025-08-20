################################################################################
# filename: view_wp.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 18/08,2025
################################################################################

import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.conf import settings

################################################################################
#CONSTANT

url = os.getenv("WP_ENDPOINT")
wp_user = os.getenv("WP_USER")
wp_app_password = os.getenv("WP_PSWD")
jwt_url = os.getenv("JWT_ENDPOINT")

################################################################################

def register_user(request):
    if request.method == "POST":
        body = json.loads(request.body)

        firstName = body.get("firstName")
        lastName = body.get("lastName")
        email = body.get("email")
        password = body.get("password")
        telephone = body.get("telephone")
        moto = body.get("moto")

        wp_response = create_wp_user(firstName, lastName, email, password, telephone, moto)

        return JsonResponse({"wordpress": wp_response})

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)

################################################################################

def get_users(request):
    response = requests.get(
        url,
        auth=(wp_user, wp_app_password),
        verify=False
    )
    answer = [get_dict_for_front(user) for user in response.json()]
    return JsonResponse({"wordpress":answer})

################################################################################

def get_user(request,id):
    response = requests.get(
        url+f"/{id}",
        auth=(wp_user, wp_app_password),
        verify=False
    )
    answer = get_dict_for_front(response.json())
    return JsonResponse({"wordpress": answer})
    

################################################################################

def connect(request):
    body = json.loads(request.body)
    response = requests.post(
        jwt_url,
        auth=(wp_user, wp_app_password),
        json={
            "username": body["username"],
            "password": body["password"],
        },
        verify=False
    )
    return JsonResponse(response.json())

################################################################################

def get_dict_for_front(user: dict):
    return {
        "id":user["id"],
        "firstName":user["slug"].split("-")[0],
        "lastName": user["slug"].split("-")[-1],
        "telephone":user["telephone"],
        "moto":user["moto"]
    }

################################################################################

def create_wp_user(firstName : str, lastName : str, email, password, telephone, moto):
    username = firstName.lower() + "." + lastName.lower()

    response = requests.post(
        url,
        auth=(wp_user, wp_app_password),
        json={
            "username": username,
            "email": email,
            "password": password,
            "roles": ["subscriber"],
            "firstName": firstName,
            "lastName": lastName,
            "telephone":telephone,
            "moto":moto,
        },
        verify=False  # si tu es en certificat auto-signé
    )
    return response.json()

################################################################################
# End of File
################################################################################