from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(Users_conversation)
admin.site.register(Status_list)
admin.site.register(Description_of_conversation)