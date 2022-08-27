from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

TYPE_CHOICES = (
        (1, 'Member'),
        (2, 'Staff'),
        (3, 'Admin'),
    )

class CustomUser(AbstractUser):
    type = models.PositiveIntegerField(choices=TYPE_CHOICES,default=1)
    description = models.TextField(max_length=300,default='Hi!')

    def __str__(self):
        return f'{self.username}'

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,primary_key=True)
    image = models.ImageField(default='default.jpg',upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
