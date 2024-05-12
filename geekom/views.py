from rest_framework import status
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import NewUser, Create_message, Create_conversation, Add_to_conversation, Users_conversation
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.decorators import renderer_classes
from rest_framework.renderers import StaticHTMLRenderer
from rest_framework_simplejwt.backends import TokenBackend
from django.forms.models import model_to_dict
import datetime
import json
import re


@csrf_exempt
@renderer_classes((StaticHTMLRenderer,))
def register(request):
    pattern = re.compile(r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$")
    if request.method == "POST":
        post = json.loads(request.body)
        email_check = User.objects.filter(email=post['email']).count()
        if re.match(pattern,post['email']) == False:
            content = {"wrong email": "wrong email"}
            return HttpResponse(content, status=status.HTTP_409_CONFLICT)
        username_check = User.objects.filter(username=post['username']).count()
        if email_check > 0:
            content = {"email taken": "email taken"}
            return HttpResponse(content, status=status.HTTP_409_CONFLICT)
        if username_check > 0:
            content = {"username taken": "username taken"}
            return HttpResponse(content, status=status.HTTP_409_CONFLICT)
        form = NewUser(post)
        if form.is_valid():
            user = form.save()
            return HttpResponse("success")
        return HttpResponse({"bad request":"bad request"}, status=status.HTTP_400_BAD_REQUEST)
    form = NewUser()
    return HttpResponse({"success":"success"}, status=status.HTTP_200_OK) 




@csrf_exempt
def Get_messages_to_conv(request):
    if request.method == "GET":
        conversation_id = int(request.GET.get('id'))
        conversation_needed = Conversation.objects.get(id=conversation_id)
        messages = list(Message.objects.filter(Conversation_id=conversation_needed).values())
        for i in messages:
            i['Sender_id'] = User.objects.get(id=int(i['Sender_id'])).get_username()
        message_first = "Wiadomości w " + conversation_needed.Name
        messages.insert(0,{"Conversation_id_id": conversation_needed.Name,
                           "Sender_id": "Admin",
                           "Message": message_first})
        return JsonResponse(messages,safe=False)
    return HttpResponse({"bad request":"bad request"}, status=status.HTTP_400_BAD_REQUEST)
   
   
@csrf_exempt
def Add_message(request):
    if request.method == "POST":
        message_post = json.loads(request.body)
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        try:
            valid_data = TokenBackend(algorithm='HS256').decode(token,verify=False)
            user_id = valid_data['user_id']
            request.user = User.objects.get(id=int(user_id))
        except ValueError as v:
            print("validation error", v)  
        message_post = {
            "Conversation_id": Conversation.objects.get(id=message_post['Conversation_id']),
            "Sender": User.objects.get(id=int(user_id)),
            "Message": message_post['Message'],
            "Date": datetime.date.today()
        }
        form = Create_message(message_post)
        if form.is_valid():
            form.save()
            return HttpResponse({"success":"success"}, status=status.HTTP_200_OK) 
    return HttpResponse({"bad request":"bad request"}, status=status.HTTP_400_BAD_REQUEST)
   
# Create your views here.

@csrf_exempt
def Create_Conversation(request: HttpRequest):
    if request.method == "POST":
        conversation_post = json.loads(request.body)
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        try:
            valid_data = TokenBackend(algorithm='HS256').decode(token,verify=False)
            user_id = valid_data['user_id']
            request.user = User.objects.get(id=int(user_id))
        except ValueError as v:
            print("validation error", v)
        
        conversation_form = {
            "Name": conversation_post['conversation_name'],
            "Key": conversation_post['encryption_key'],
            "Creator": request.user
        }
        form = Create_conversation(conversation_form)
        if form.is_valid():
            coversation_model = form.save()
        
            user_to_conf_form = {
                "User_id": request.user,
                "Conversation_id": coversation_model,
                "Administrator": True
            }
            form2 = Add_to_conversation(user_to_conf_form)
            if form2.is_valid():
                form2.save()
                return HttpResponse({"success":"success"}, status=status.HTTP_200_OK) 
        return HttpResponse({"bad request":"bad request"}, status=status.HTTP_400_BAD_REQUEST)
        
        
@csrf_exempt
def Add_user_to_conf(requset: HttpRequest):
    if requset.method == "POST":
        post_information = json.loads(requset.body)
        user_to_conf_form = {
            "User_id": User.objects.get(username=post_information['User_id']),
            "Conversation_id": Conversation.objects.get(id=post_information["Conversation_id"]),
            "Administrator": False
        }
        form = Add_to_conversation(user_to_conf_form)
        if form.is_valid():
            form.save()
            return HttpResponse({"success":"success"}, status=status.HTTP_200_OK) 
        return HttpResponse({"bad request":"bad request"}, status=status.HTTP_400_BAD_REQUEST)
    
    
@csrf_exempt
def Get_user_conversation(request):
    if request.method == "GET":
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        try:
            valid_data = TokenBackend(algorithm='HS256').decode(token,verify=False)
            user_id = valid_data['user_id']
            request.user = User.objects.get(id=int(user_id))
        except ValueError as v:
            print("validation error", v)
        converasations_list = []
        
        converasations_id = list(Users_conversation.objects.filter(User_id=request.user).values())
        for i in converasations_id:
            holder = {
                "Conversation_id": i['Conversation_id_id'],
                "conversation_name": Conversation.objects.get(id=int(i['Conversation_id_id'])).Name,
                "User_id":  User.objects.get(id=int(i['User_id_id'])).get_username()
            }
            converasations_list.append(holder)
        return JsonResponse(converasations_list,safe=False)
    return HttpResponse({"bad request":"bad request"}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def User_info(request: HttpRequest):
    if request.method == "GET":
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        try:
            valid_data = TokenBackend(algorithm='HS256').decode(token,verify=False)
            user_id = valid_data['user_id']
            request.user = User.objects.get(id=int(user_id))
        except ValueError as v:
            print("validation error", v)
        nick = {
            "nick": request.user.get_username()
        }
        return JsonResponse(nick,safe=False)