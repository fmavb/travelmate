from django import forms
from django.forms import DateInput

from app.models import Trip, Destination, UserProfile

class Settings(forms.ModelForm):
    # CharField, since AutoComplete works with text
    homeCountryText = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'destination', 'placeholder': 'Type Country/State'}))
    public = forms.BooleanField(required=False)
    profilePic = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ('profilePic','public',)

class TripForm(forms.ModelForm):
	public = forms.BooleanField(required=False)
	# CharField, since AutoComplete works with text
	destinationText = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'destination', 'placeholder': 'Type Country/State'}))

	class Meta:
		model = Trip
		# DateInput widgets
		widgets = {'startDate': DateInput(attrs={'class': 'datepicker'}),
		           'endDate': DateInput(attrs={'class': 'datepicker'}),
		           }
		fields = ('startDate', 'endDate', 'public')