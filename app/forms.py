from django import forms
from django.forms import DateInput

from app.models import Trip, Destination, UserProfile

class Settings(forms.ModelForm):
    homeCountry = forms.ModelChoiceField(queryset=Destination.objects.all().order_by('name'), required=True,
                                         initial=Destination.objects.get(name__exact="United Kingdom"))
    public = forms.BooleanField(required=False)
    profilePic = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ('homeCountry','profilePic','public',)

class TripForm(forms.ModelForm):
	public = forms.BooleanField(required=False)
	destination = forms.ModelChoiceField(queryset=Destination.objects.all())

	class Meta:
		model = Trip
		widgets = {'startDate': DateInput(attrs={'class': 'datepicker'}),
		           'endDate': DateInput(attrs={'class': 'datepicker'}),
		           }
		fields = ('startDate', 'endDate', 'public', 'destination')