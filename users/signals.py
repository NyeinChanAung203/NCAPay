from django.db.models.signals import pre_save,post_save
from .models import User
from django.dispatch import receiver
from pay.models import Wallet
from django_user_agents.utils import get_user_agent

def acc_num_generator(phone):
    acc_num = hash(str(phone))
    return str(acc_num)[1:16]

@receiver(pre_save,sender=User)
def pre_save_user_accnum(sender,instance,**kwargs):
    print('user pre save')
    instance.acc_num = acc_num_generator(instance.phone)
    print('Saving')


@receiver(post_save,sender=User)
def post_save_user_wallet(sender,instance,created,**kwargs):
    if created:
        Wallet.objects.create(
            account_number = instance.acc_num,
            account_person = instance,
            amount=0
        )
    print('post save wallet')