from django.forms import ModelForm,Textarea
from django import forms
from .models import Transaction


class TransactionForm(forms.Form):
    to_user = forms.CharField(max_length=11,required=True,label="To")
    amount = forms.IntegerField(min_value=500)
    description = forms.CharField(required=False,widget=Textarea())

    to_user.widget.attrs.update({'placeholder':'09********'})