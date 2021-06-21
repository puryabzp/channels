from django.contrib import admin
from .models import GroupChat,Member,Message

# Register your models here.
admin.site.register(Message)
admin.site.register(Member)
admin.site.register(GroupChat)
