from django.db import models

# Create your models here.

class Sites(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.code} AKA {self.name} "

class Vessel(models.Model):
    takeoff = models.ForeignKey(Sites, on_delete=models.CASCADE, related_name="departures")
    land = models.ForeignKey(Sites, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()

    def __str__(self):
        return f"Vessel [{self.id}]  {self.takeoff} --> {self.land}"