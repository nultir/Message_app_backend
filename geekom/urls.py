from django.urls import path

from . import views



urlpatterns = [
    path('conversation/messages/get_messages', views.Get_messages_to_conv, name="message_to_conversation"),
    path('user/registration', views.register, name="register"),
    path('conversation/create_converastion', views.Create_Conversation, name="con_create"),
    
    
]
