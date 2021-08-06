from django import forms
from django.forms import widgets
from django.forms.forms import Form
from .models import Order,Customer
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.admin import widgets

class CheckoutForm(forms.ModelForm):
    date= forms.DateField(widget=forms.SelectDateWidget)
    # Time =forms.TimeField(widget=widgets.SelectTimeWidget())
    
    class Meta:
        model = Order
        fields = ["ordered_by", "address", "mobile", "email","date" ,"Time"]

      
class CustomerRergistationForm(forms.ModelForm):
    # username = forms.CharField(widget=forms.TextInput())
    email = forms.CharField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())
  
    class Meta:
        model = Customer
        fields = ["email", "password", "full_name", "address"]

    # def clean_email(self):
    #     uem = self.cleaned_data.get("email")
    #     if User.objects.filter(email=uem).exists():
    #         raise forms.ValidationError(" Customer with Same Email Id already exist. ")
    #     return uem
class CustomerLoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

        