from django import forms
from django.forms import DateInput, Textarea

from app.models import Trip, UserProfile, BlogPost, PostImage, Comment, Rating

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
		widgets = {'startDate': DateInput(attrs={'class': 'start form-control', 'placeholder': 'Please select start of Trip (mm/dd/yyyy)', 'required':'required'}),
		           'endDate': DateInput(attrs={'class': 'end form-control', 'placeholder': 'Please select end of Trip (mm/dd/yyyy)', 'required':'required'}),
		           }
		fields = ('title', 'startDate', 'endDate', 'public')

class BlogForm(forms.ModelForm):
	title = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Give your blogpost a title!'}))
	content = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows':8, 'class':'form-control', 'placeholder': 'Give your trip some content!'}))
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)

	class Meta:
		model = BlogPost
		fields = ('title', 'content')

class PhotoForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ('image', )

class CommentForm(forms.ModelForm):
	content = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':4, 'class':'form-control', 'placeholder': 'Write Comment...'}))

	class Meta:
		model = Comment
		fields = ('content', )

SCORES= [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
	('5', '5'),
    ]

class RatingForm(forms.ModelForm):
	score = forms.CharField(required=False, widget=forms.RadioSelect(choices=SCORES))

	class Meta:
		model = Rating
		fields = ('score', )