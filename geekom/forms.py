from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class NewUser(UserCreationForm):
    
    email = forms.EmailField(required=True)

    
    class Meta:
        model = User
        
        fields = ("username","email","password1","password2")
        
    def save(self, commit=True):
        user = super(NewUser, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
    
class Create_message(ModelForm):
    Conversation_id = forms.ModelChoiceField(queryset=Conversation.objects.all())
    Sender = forms.ModelChoiceField(queryset=User.objects.all())
    Message = forms.CharField()
    Date = forms.DateTimeField()
    
    class Meta:
        model = Message
        
        fields = ['Conversation_id','Message','Sender','Date']


class Create_conversation(ModelForm):
    Name = forms.CharField()
    Key = forms.CharField()
    Creator = forms.ModelChoiceField(queryset=User.objects.all())
    class Meta:
        model = Conversation
        fields = ["Name","Key","Creator"]
        
#xd

class Add_to_conversation(ModelForm):
    User_id = forms.ModelChoiceField(queryset=User.objects.all())
    Conversation_id = forms.ModelChoiceField(queryset=Conversation.objects.all())
    
    class Meta:
        model = Users_conversation
        
        fields = ["User_id","Conversation_id"]
        

class Add_user_to_friends(ModelForm):
    User_1 = forms.ModelChoiceField(queryset=User.objects.all())
    User_2 = forms.ModelChoiceField(queryset=User.objects.all())
    Status = forms.CharField()
    
    class Meta:
        model = Status_list
        
        fields = ["User_1","User_2","Status"]
        

class Add_description_conversation(ModelForm):
    Conversation_id = forms.ModelChoiceField(queryset=Conversation.objects.all())
    Description = forms.CharField()
    
    class Meta:
        model = Description_of_conversation
        
        fields = ["Conversation_id","Description"]
        

class Add_Avatar(ModelForm):
    User_id = forms.ModelChoiceField(queryset=User.objects.all())
    Avatar = forms.ImageField()
    class Meta:
        model = Avatar
        
        fields = ["User_id","Avatar"]
        

class Add_User_description(ModelForm):
    User_id = forms.ModelChoiceField(queryset=User.objects.all())
    Description = forms.CharField()
    class Meta:
        model = Description_of_User
        
        fields = ["User_id","Description"]