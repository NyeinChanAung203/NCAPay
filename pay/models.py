from django.db import models
from users.models import User

# # Create your models here.
class Wallet(models.Model):
    account_number = models.CharField(verbose_name="Account Number",max_length=25)
    account_person = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.account_person.name} ({self.amount} MMK)'


TRANSFER_TYPE = (
    ('Expense','Expense'),
    ('Income','Income')
)
class Transaction(models.Model):
    ref_no = models.CharField(max_length=16,null=True)
    trx_id = models.CharField(max_length=16,null=True)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    to_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="receiver")
    transfer_type = models.CharField(choices=TRANSFER_TYPE,max_length=8,default="Expense")
    amount = models.PositiveIntegerField()
    description = models.TextField(blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        if(self.transfer_type == "Expense"):
            return f'{self.from_user} to {self.to_user}'
        else:
            return f'{self.from_user} from {self.to_user}'

    class Meta:
        ordering = ['-created',]

NOTI_TYPE = (
    ('Unread','Unread'),
    ('Read','Read')
)
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    transfer_type = models.CharField(choices=TRANSFER_TYPE,max_length=8,null=True)
    data = models.CharField(max_length=120)
    noti_type = models.CharField(choices=NOTI_TYPE,max_length=6,default='Unread',null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    @property
    def get_unread(self):
        return self.noti_type

    def __str__(self):
        return self.data
    
    class Meta:
        ordering = ['-created',]

