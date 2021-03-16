from django import forms

from my_profile.models import EmailMessage


class SendEmailForm(forms.ModelForm):
    class Meta:
        model = EmailMessage
        fields = ['name', 'email', 'subject', 'message']
