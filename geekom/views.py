from rest_framework import status
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import NewUser, Create_message, Create_conversation, Add_to_conversation, Users_conversation,Add_description_conversation
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.decorators import renderer_classes
from rest_framework.renderers import StaticHTMLRenderer
from rest_framework_simplejwt.backends import TokenBackend
from django.forms.models import model_to_dict
import datetime
import json
import re



def token_veryfication(token):
    try:
        valid_data = TokenBackend(algorithm='HS256').decode(token,verify=False)
        user_id = valid_data['user_id']
        return User.objects.get(id=int(user_id))
    except ValueError as v:
        print("validation error", v)


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
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        request.user = token_veryfication(token)
        conversation_id = int(request.GET.get('id'))
        conversation_needed = Conversation.objects.get(id=conversation_id)
        messages = list(Message.objects.filter(Conversation_id=conversation_needed).values())
        check_in_conv = Users_conversation.objects.filter(User_id=request.user,Conversation_id=conversation_id).exists()
        check_decripton = Description_of_conversation.objects.filter(Conversation_id=conversation_id).exists()
        if check_decripton:
            description = Description_of_conversation.objects.get(Conversation_id=conversation_id).Description
        else:
            description = "brak description"
        if check_in_conv:
            check_block = Users_conversation.objects.get(User_id=request.user,Conversation_id=conversation_id).If_blocked
            if not check_block:
                for i in messages:
                    i['Sender_id'] = User.objects.get(id=int(i['Sender_id'])).get_username()
                message_first = "Wiadomości w " + conversation_needed.Name
                messages.insert(0,{"Conversation_id_id": conversation_needed.Name,
                                "Sender_id": "Admin",
                                "Message": message_first,
                                "Description": description})      
            else:
               messages = [{"Conversation_id_id": "BLOCK",
                            "Sender_id": "Admin",
                            "Message": "You are blocked",
                            "Description": "BLOCK"}]
        else:
            messages = [{"Conversation_id_id": "Error",
                            "Sender_id": "Admin",
                            "Message": "Cannot Acces",
                            "Description": "Error"}]
        return JsonResponse(messages,safe=False)
    return HttpResponse({"bad request":"bad request"}, status=status.HTTP_400_BAD_REQUEST)
   
   
@csrf_exempt
def Add_message(request):
    if request.method == "POST":
        message_post = json.loads(request.body)
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        request.user = token_veryfication(token) 
        date = datetime.datetime.now()
        message_post = {
            "Conversation_id": Conversation.objects.get(id=message_post['Conversation_id']),
            "Sender": request.user,
            "Message": message_post['Message'],
            "Date": date
        }
        print(date)
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
        request.user = token_veryfication(token)
        
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
            }
            form2 = Add_to_conversation(user_to_conf_form)
            if form2.is_valid():
                model = form2.save()
                model.Administrator = True
                model.save()
                return HttpResponse({"success":"success"}, status=status.HTTP_200_OK) 
            
        return HttpResponse({"bad request":"bad request"}, status=status.HTTP_400_BAD_REQUEST)
        
        
@csrf_exempt
def Add_user_to_conf(requset: HttpRequest):
    if requset.method == "POST":
        post_information = json.loads(requset.body)
        Conversation_id = Conversation.objects.get(id=post_information["id"])
        user = User.objects.get(username=post_information['users'])
        check_if_added = Users_conversation.objects.filter(User_id=user,Conversation_id=Conversation_id).exists()
        if check_if_added:
            return HttpResponse({"bad request":"bad request"}, status=status.HTTP_400_BAD_REQUEST)
        user_to_conf_form = {
            "User_id": User.objects.get(username=post_information['users']),
            "Conversation_id": Conversation.objects.get(id=post_information["id"]),
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
        print(token)
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
                "User_id":  User.objects.get(id=int(i['User_id_id'])).get_username(),
                "Administrator": i["Administrator"]
            }
            converasations_list.append(holder)
        return JsonResponse(converasations_list,safe=False)
    return HttpResponse({"bad request":"bad request"}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def User_info(request: HttpRequest):
    if request.method == "GET":
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        request.user = token_veryfication(token)
        Description = "Desc"
        if Description_of_User.objects.filter(User_id=request.user).exists():
            Description = Description_of_User.objects.get(User_id=request.user).Description
        nick = {
            "nick": request.user.get_username(),
            "Description": Description
        }
        return JsonResponse(nick,safe=False)

@csrf_exempt
def Conversation_user_info(request: HttpRequest):
    if request.method == "GET":
        converastion_get_id = int(request.GET.get('id'))
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        request.user = token_veryfication(token)
        
        users = list(Users_conversation.objects.filter(Conversation_id=converastion_get_id).values()) 
        for i in users:
            if Description_of_User.objects.filter(User_id=i['User_id_id']).exists():
                i.update({"Description": Description_of_User.objects.get(User_id=i['User_id_id']).Description})
            else:
                i.update({"Description": "Brak opisu"})
            i['User_id_id'] = User.objects.get(id=i['User_id_id']).get_username()
            if i["If_blocked"] == True:
                users.remove(i)
           
        return JsonResponse(users,safe=False)
    
    
    
@csrf_exempt
def Block_from_conversation(request: HttpRequest):
    if request.method == "POST":

        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        request.user = token_veryfication(token)
            
        
        post_information = json.loads(request.body)
        converastion_id = int(post_information['id'])
        username = post_information['username']
        if username == request.user.get_username():
            return HttpResponse({"bad request":"bad request"}, status=status.HTTP_400_BAD_REQUEST)
        if Users_conversation.objects.get(Conversation_id=converastion_id,User_id=request.user).Administrator:
            blocked_user = User.objects.get(username=username)
            relation = Users_conversation.objects.get(Conversation_id=converastion_id,User_id=blocked_user)
            relation.If_blocked = True
            relation.save()
            return HttpResponse('success')
    return HttpResponse({"bad request":"bad request"}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def Remove_conversation(request: HttpRequest):
    if request.method == "POST":
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        request.user = token_veryfication(token)
        
        post_information = json.loads(request.body)
        conversation = Conversation.objects.get(id=post_information['id'])
        user_conversation = Users_conversation.objects.get(Conversation_id=conversation,User_id=request.user)
        if user_conversation.Administrator == True:
            conversation.delete()
            return HttpResponse('success')
    return HttpResponse({"bad request":"bad request"}, status=status.HTTP_400_BAD_REQUEST)
    
@csrf_exempt
def Leave_conversation(request: HttpRequest):
    if request.method == "POST":
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        request.user = token_veryfication(token)
    
        post_information = json.loads(request.body)
        conversation = Conversation.objects.get(id=post_information['id'])
        Users_conversation.objects.get(Conversation_id=conversation,User_id=request.user).delete()
        return HttpResponse('success')
    return HttpResponse({"bad request":"bad request"}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def Add_description(request: HttpRequest):
    if request.method == "POST":
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        request.user = token_veryfication(token)

        post_information = json.loads(request.body)
        Conversation_id = Conversation.objects.get(id=post_information["id"])
        user_conversation = Users_conversation.objects.get(Conversation_id=Conversation_id,User_id=request.user)
        if Description_of_conversation.objects.filter(Conversation_id=Conversation_id).exists():
            Description_of_conversation.objects.get(Conversation_id=Conversation_id).delete()
         
        if user_conversation.Administrator == True:
            form_description = {
                "Conversation_id": Conversation_id,
                "Description": post_information["Description"]
            }
            form = Add_description_conversation(form_description)
            if form.is_valid():
                form.save()
                return HttpResponse('success')
    return HttpResponse({"bad request":"bad request"}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def Add_description_user(request: HttpRequest):
    if request.method == "POST":
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        request.user = token_veryfication(token)

        post_information = json.loads(request.body)
        if Description_of_User.objects.filter(User_id=request.user).exists():
            Description_of_User.objects.get(User_id=request.user).delete()
         
        form_description = {
            "User_id": request.user,
            "Description": post_information["Description"]
        }
        form = Add_description(form_description)
        if form.is_valid():
            form.save()
            return HttpResponse('success')
    return HttpResponse({"bad request":"bad request"}, status=status.HTTP_400_BAD_REQUEST)
