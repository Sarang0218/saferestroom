from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django.conf import settings
# Create your models here.
class Review(models.Model):
    sanitation_score = models.IntegerField()
    safe_score = models.IntegerField()
    suggest_score = models.IntegerField()

   

class Building(models.Model):
    title = models.CharField(max_length=50)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="building")

class Restroom(models.Model):

    title = models.CharField(max_length=30)
    key = models.CharField(max_length=32)
    building = models.ForeignKey(
      Building,
      on_delete=models.CASCADE
    ) 
    location_information = models.CharField(max_length=30, null=True)
    reviews = models.ManyToManyField(
        Review,
        blank=True
    )
    

class PrivateRestroom(models.Model):
    
    restroom = models.ForeignKey(
        Restroom,
        on_delete=models.CASCADE
      )
    time_left = models.IntegerField()
    
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    def __str__(self):
      return self.restroom.title
    
    
class RestroomVisitData(models.Model):
    p_restroom = models.ForeignKey(
        PrivateRestroom,
        on_delete=models.CASCADE,
        null=True
      )
    GENDER_CHOICES = (
        ('M', '남성'),
        ('F', '여성'),
    )
    telephone = models.CharField(max_length=30)
    
    made_time = models.DateTimeField(null=True, default=timezone.now)
    
    link_recieved_time = models.DateTimeField(null=True, blank=True)
    qr_open_time = models.DateTimeField(null=True, blank=True)
    qr_scan_time = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    qr = models.CharField(max_length=150, null=True)
    active = models.BooleanField(default=True)
    

