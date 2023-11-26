from django.contrib import admin

from .models import Notification, Subscription
# Register your models here.
admin.site.register(Notification)
admin.site.register(Subscription)