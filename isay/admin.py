from django.contrib import admin
from .models import Appointment,Profile,ThreadModel,MessageModel
# Register your models here.

admin.site.register(Appointment)
admin.site.register(Profile)
admin.site.register(ThreadModel)
admin.site.register(MessageModel)
