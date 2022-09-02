from django.db import models
from django.urls import reverse
from users.models import CustomUser

# Create your models here.

class Sport(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    image = models.ImageField(default='sport.jpg',upload_to='sport_pics')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('sport-detail',kwargs={'sportid':self.pk})

class Court(models.Model):
    name = models.CharField(max_length=100)
    sport = models.ForeignKey(Sport,on_delete=models.CASCADE)
    image = models.ImageField(default='court.jpg',upload_to='court_pics')
    rating = models.FloatField(default=0)
    capacity = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('sport-detail',kwargs={'sportid':self.sport.pk})

class Slot(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    court = models.ForeignKey(Court,on_delete=models.CASCADE)
    avail = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.start} {self.end} {self.court}'

STAT_CHOICES = (
    (0,'Rejected'),
    (1, 'Accepted'),
)

class UserBooking(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot,on_delete=models.CASCADE)
    booking_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    status = models.PositiveIntegerField(choices=STAT_CHOICES)

class Item(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(default='item.jpg',upload_to='item_pics')
    sport = models.ForeignKey(Sport,on_delete=models.CASCADE)
    number = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('sport-detail',kwargs={'sportid':self.sport.pk})



