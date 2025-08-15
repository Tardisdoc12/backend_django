################################################################################
# filename: views.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 13/08,2025
################################################################################

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Inscrit, UserEvent
import json

################################################################################

@csrf_exempt
def list_events(request):
    inscrits = Inscrit.objects.all()
    seen=[]
    inscritsJson = []
    for inscrit in inscrits:
        d = inscrit.getJson()
        event = inscrit.event.getJson()
        if event not in seen:
            seen.append(event)
            inscritsJson.append(d)
    events = Event.objects.all()
    for event in events:
        eventJson = event.getJson()
        if eventJson not in seen:
            seen.append(eventJson)
            inscritsJson.append({**eventJson, "users":[]})
    return JsonResponse(inscritsJson, safe=False)

# @csrf_exempt
# def list_events(request):
#     events = Event.objects.all().values()
#     for event in events:
#         users = UserEvent.objects.filter(inscrit__event_id=event["id"])
#         users_list = [u.getJson() for u in users]
#         event["users"] = users_list
#     return JsonResponse(list(events), safe=False)

################################################################################

@csrf_exempt
def create_event(request):
    if request.method == "POST":
        data = json.loads(request.body)
        event = Event.objects.create(
            title=data.get("title"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            description=data.get("description"),
            place=data.get("place"),
            category=data.get("category"),
            subscribe_places=data.get("subscribe_places"),
            nonsubscribe_places=data.get("nonsubscribe_places"),
        )
        return JsonResponse({"id": event.id, "title": event.title})
    return JsonResponse({"error": "Method not allowed"}, status=405)

################################################################################

@csrf_exempt
def delete_event(request, event_id):
    if request.method == "DELETE":
        try:
            event = Event.objects.get(id=event_id)
            event.delete()
            return JsonResponse({"message": "Event deleted"})
        except Event.DoesNotExist:
            return JsonResponse({"error": "Event not found"}, status=404)
    return JsonResponse({"error": "Method not allowed"}, status=405)

################################################################################

@csrf_exempt
def get_list_inscript(request, event_id):
    try:
        inscrits = Inscrit.objects.filter(event_id=event_id)
        seen=[]
        inscritsJson = []
        for inscrit in inscrits:
            d = inscrit.getJson()
            event = inscrit.event.getJson()
            if event not in seen:
                seen.append(event)
                inscritsJson.append(d)
        return JsonResponse({"inscrit": inscritsJson},status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

################################################################################

@csrf_exempt
def create_inscrit(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            event_id = data.get("event_id")
            user_data = data.get("user")

            # Vérifie que l'événement existe
            try:
                event = Event.objects.get(id=event_id)
            except Event.DoesNotExist:
                return JsonResponse({"error": "Event not found"}, status=404)

            # Cherche un utilisateur existant par email, sinon le crée
            user_event, created = UserEvent.objects.get_or_create(
                email=user_data["email"],
                defaults={
                    "name": user_data["name"],
                    "phone": user_data["phone"],
                    "experience": user_data["experience"],
                }
            )

            # Crée l'inscription (ou empêche les doublons)
            inscrit, created = Inscrit.objects.get_or_create(
                user=user_event,
                event=event,
                bike= user_data["bike"],
                goal= user_data["goal"],
            )

            if not created:
                return JsonResponse({"error": "User already registered for this event"}, status=400)

            return JsonResponse({"message": "Inscription created", "event": event.getJson()})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)

################################################################################
# End of File
################################################################################