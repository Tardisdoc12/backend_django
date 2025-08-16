################################################################################
# filename: models.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 13/08,2025
################################################################################

from django.db import models

################################################################################

class Event(models.Model):
    title = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField()
    place = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    subscribe_places = models.IntegerField()
    nonsubscribe_places = models.PositiveIntegerField()

    def __str__(self):
        return self.title
    
    def getJson(self):
        return {
            "id": self.id,
            "title": self.title,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description,
            "place": self.place,
            "category": self.category,
            "subscribe_places": self.subscribe_places,
            "nonsubscribe_places": self.nonsubscribe_places,
        }

################################################################################

class UserEvent(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    email = models.CharField(max_length=200)
    experience = models.CharField(max_length=200)
    

    def getJson(self):
        return {
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "experience": self.experience
        }

################################################################################

class Inscrit(models.Model):
    user = models.ForeignKey(UserEvent, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date_inscription = models.DateTimeField(auto_now_add=True)
    bike = models.CharField(max_length=200, null=True, blank=True)
    goal = models.CharField(null=True, blank=True, max_length=200)

    class Meta:
        unique_together = ('user', 'event')  # Empêche un utilisateur de s'inscrire deux fois au même événement

    def getJson(self):
        inscrits = Inscrit.objects.filter(event=self.event)
        users_list = [{**i.user.getJson(), "bike":self.bike,"goal":self.goal} for i in inscrits]

        # On prend les infos de l'événement et on y ajoute les inscrits
        event_data = self.event.getJson()
        event_data["users"] = users_list

        return event_data

################################################################################
# End of File
################################################################################