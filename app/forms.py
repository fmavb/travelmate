from django import forms
from app.models import UserProfile, Destination
from django.contrib.auth.models import User

class Settings(forms.ModelForm):
    homeCountry = forms.ModelChoiceField(queryset=Destination.objects.all().order_by('name'), required=True,
                                         initial="United Kingdom")
    class Meta:
        model = UserProfile
        fields = ('user','homeCountry','profilePic','public',)