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
	public = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'checkbox'}))
	# CharField, since AutoComplete works with text
	destinationText = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'destination', 'placeholder': 'Type Country/State'}))

	class Meta:
		model = Trip
		# DateInput widgets
		widgets = {'startDate': DateInput(attrs={'class': 'start'}),
		           'endDate': DateInput(attrs={'class': 'end'}),
		           }
		fields = ('startDate', 'endDate', 'public')