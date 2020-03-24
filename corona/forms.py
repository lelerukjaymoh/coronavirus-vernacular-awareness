from django import forms
from .models import Recipient, Language, Donation, Volunteer, Message, VernacularMessage

class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['phone_number',]
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': '0712345678'}),
        }
        labels = {
            'phone_number': ''
        }
    
class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ['names', 'language', 'phone']
        widgets = {
            'names': forms.TextInput(attrs={'placeholder': 'Names'}),
            'language': forms.TextInput(attrs={'placeholder': 'Langauge'}),
            'phone': forms.TextInput(attrs={'placeholder': '071234578'}),
        }
        labels = {
            'names': '', 'language': '', 'phone': ''
        }

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['donor', 'amount', 'phone_number']
        widgets = {
            'donor': forms.TextInput(attrs={'placeholder': 'Names'}),
            'amount': forms.TextInput(attrs={'placeholder': '1000'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '071234578'}),
        }
        labels = {
            'donor': '', 'amount': '', 'phone_number': ''
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['language', 'main_message']
        widgets = {
            'language': forms.TextInput(attrs={'placeholder': 'Langauge'}),
            'main_message': forms.TextInput(attrs={'placeholder': 'Main Message ...'}),
        }
        labels = {
            'language': '', 'main_message': ''
        }

class VernacularMessageForm(forms.ModelForm):
    class Meta:
        model = VernacularMessage
        fields = ['language', 'message']
        widgets = {
            'language': forms.TextInput(attrs={'placeholder': 'Langauge'}),
            'message': forms.TextInput(attrs={'placeholder': 'Vernacular Message ...'}),
        }
        labels = {
            'language': '', 'message': ''
        }

