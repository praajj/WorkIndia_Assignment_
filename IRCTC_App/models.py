from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username

class Train(models.Model):
    train_name = models.CharField(max_length=100, unique=True)
    train_number = models.CharField(max_length=10, unique=True)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    total_seats = models.IntegerField(default=0)
    booked_seats = models.IntegerField(default=0) 
    created_at = models.DateTimeField(auto_now_add=True)
    def available_seats(self):
        return self.total_seats - self.booked_seats