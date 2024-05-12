from django.urls import path

from . import views



urlpatterns = [
    path('conversation/messages/get_messages', views.Get_messages_to_conv, name="message_to_conversation"),
    path('conversation/messages/create_message', views.Add_message, name="message_to_conversation"),
    path('user/registration', views.register, name="register"),
    path('user/info', views.User_info, name="info"),
    path('conversation/create_converastion', views.Create_Conversation, name="con_create"),
    path('conversation/user/add', views.Add_user_to_conf, name="con_create"),
    path('conversation/get_conversation', views.Get_user_conversation, name="conversation_user"),
    
    
]
