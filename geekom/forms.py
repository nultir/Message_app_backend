from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Message,Conversation,Users_conversation,Status_list


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
    Date = forms.DateField()
    
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
        

class Add_to_conversation(ModelForm):
    User_id = forms.ModelChoiceField(queryset=User.objects.all())
    Conversation_id = forms.ModelChoiceField(queryset=Conversation.objects.all())
    Administrator = forms.BooleanField()
    
    class Meta:
        model = Users_conversation
        
        fields = ["User_id","Conversation_id","Administrator"]
        

class Add_user_to_friends(ModelForm):
    User_1 = forms.ModelChoiceField(queryset=User.objects.all())
    User_2 = forms.ModelChoiceField(queryset=User.objects.all())
    Status = forms.CharField()
    
    class Meta:
        model = Status_list
        
        fields = ["User_1","User_2","Status"]