from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save,post_save 

class User(AbstractUser):
    name = models.CharField(max_length=120,null=True)
    email = models.EmailField(unique=True,null=True)
    phone = models.CharField(unique=True,max_length=11,null=True)
    acc_num = models.CharField(max_length=25,blank=True,null=True)
    ip_address = models.CharField(max_length=100,null=True,blank=True)
    user_agent = models.CharField(max_length=120,null=True,blank=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.name}({self.phone})'

def acc_num_generator(phone):
    acc_num = hash(str(phone))
    return str(acc_num)[1:16]


