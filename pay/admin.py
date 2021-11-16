from django.contrib import admin
from .models import Transaction,Wallet,Notification
# # Register your models here.

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('from_user','transfer_type','to_user','amount')
    list_filter = ('transfer_type','from_user','to_user')
    search_fields = ('from_user','transfer_type','to_user')
admin.site.register(Transaction,TransactionAdmin)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user','transfer_type','noti_type')
    list_filter = ('noti_type','transfer_type','user')
admin.site.register(Notification,NotificationAdmin)


admin.site.register(Wallet)