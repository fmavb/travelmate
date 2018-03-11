from django import forms
from django.forms import DateInput

from app.models import Trip, Destination, UserProfile, BlogPost

class Settings(forms.ModelForm):
    # CharField, since AutoComplete works with text
    homeCountryText = forms.CharField(required=True, widget=forms.TextInput(attrs={'id':'country', 'class':'destination form-control', 'placeholder': 'Type Country/State'}))
    public = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'public'}))
    profilePic = forms.ImageField(required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput(attrs={'class':'upload'}))

    class Meta:
        model = UserProfile
        fields = ('profilePic','public',)

class TripForm(forms.ModelForm):
	public = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'public'}))
	# CharField, since AutoComplete works with text
	destinationText = forms.CharField(required=True, widget=forms.TextInput(attrs={'id':'country', 'class':'destination form-control', 'placeholder': 'Type Country/State'}))
	title = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Give your trip a title!'}))
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)

	class Meta:
		model = Trip
		# DateInput widgets
		widgets = {'startDate': DateInput(attrs={'class': 'start form-control', 'placeholder': 'Please select start of Trip', 'readonly':'readonly'}),
		           'endDate': DateInput(attrs={'class': 'end form-control', 'placeholder': 'Please select end of Trip', 'readonly':'readonly'}),
		           }
		fields = ('title', 'startDate', 'endDate', 'public')

class BlogForm(forms.ModelForm):
	public = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'public'}))
	# CharField, since AutoComplete works with text
	title = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Give your blogpost a title!'}))
	content = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Give your blogpost some content!'}))
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)

	class Meta:
		model = BlogPost
		# DateInput widgets

		fields = ('title', 'content')