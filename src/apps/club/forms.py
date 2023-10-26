from django import forms
from phonenumber_field.formfields import PhoneNumberField
from . import models


class TransactionAddForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)
    phonenumber = PhoneNumberField(region='IR')
    amount = forms.IntegerField()