from django import forms
from django.forms import DateInput

from app.models import Trip, Destination

class TripForm(forms.ModelForm):
	public = forms.BooleanField()
	destination = forms.ModelChoiceField(queryset=Destination.objects.all())

	class Meta:
		model = Trip
		widgets = {'startDate': DateInput(attrs={'class': 'datepicker'}),
		           'endDate': DateInput(attrs={'class': 'datepicker'}),
		           }
		fields = ('startDate', 'endDate', 'public', 'destination')