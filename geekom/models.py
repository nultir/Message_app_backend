from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Avatar(models.Model):
    User_id = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    Avatar = models.CharField(max_length=200, null=True)
     


class Conversation(models.Model):
    Conversation_unique_id = models.CharField(max_length=200, null=True)
    Owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    If_group = models.BooleanField(default=False)
    
    
class Message(models.Model):
    Conversation_id = models.ForeignKey(Conversation, on_delete=models.CASCADE, null=True)
    Message = models.CharField(max_length=500, null=True)
    Sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    
class Users_conversation(models.Model):
    User_id = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    Conversation_id = models.ForeignKey(Conversation,on_delete=models.CASCADE, null=True)
    If_blocked = models.BooleanField(default=False)