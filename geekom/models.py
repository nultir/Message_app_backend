from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy

#create file system

def folder_path(instance, filename):
    Message = instance.Message_unique_id
    conversation = instance.Conversation_id
    user_id = instance.Sender
    base, file_extenstion = filename.split(".")
    new_filename = "%s-%s-%s.%s" %(user_id,conversation,Message, file_extenstion)
    return "Image/%s/%s" %(conversation,new_filename)
    

# Create your models here.

    

class Avatar(models.Model):
    User_id = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    Avatar = models.ImageField(upload_to="avatars", null=True)
     


class Conversation(models.Model):
    Name = models.CharField(max_length=500, null=True)
    Key = models.CharField(max_length=500, null=True)
    Creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    If_group = models.BooleanField(default=False)
    
    
class Message(models.Model):
    Conversation_id = models.ForeignKey(Conversation, on_delete=models.CASCADE, null=True)
    Date = models.DateField()
    Message = models.CharField(max_length=500, null=True)
    Sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to=folder_path,default=None)
    
class Users_conversation(models.Model):
    User_id = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    Conversation_id = models.ForeignKey(Conversation,on_delete=models.CASCADE, null=True)
    Administrator = models.BooleanField(default=False, null=True)
    If_blocked = models.BooleanField(default=False)
    
class Status_list(models.Model):
    class status_enum(models.TextChoices):
        BLOCEKED = 'BL', gettext_lazy("Blocked")
        FRIEND = 'FR', gettext_lazy("Friend")
        NO_RELATION = "NR", gettext_lazy("No relation")
    
    User_1 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="first")
    User_2 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="second")
    Status = models.CharField(max_length=2,choices=status_enum.choices, default=status_enum.NO_RELATION)
    
