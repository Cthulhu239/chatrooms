from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Room(models.Model):
    room_name = models.CharField(max_length = 255)
    def __str__(self):
         return self.room_name


class Message(models.Model):
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    author = models.ForeignKey(User,on_delete = models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now = True)
    def __str__(self):
         return self.message

