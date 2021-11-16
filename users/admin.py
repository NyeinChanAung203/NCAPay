from django.contrib import admin
from .models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('name','email','phone')
    search_fields = ('name','email','phone')

admin.site.register(User,UserAdmin)