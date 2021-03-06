from django import forms
from django.forms import DateInput, Textarea

from app.models import Trip, UserProfile, BlogPost, PostImage, Comment, Rating


class Settings(forms.ModelForm):
    # CharField, since AutoComplete works with text
    homeCountryText = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'id': 'country', 'class': 'destination form-control', 'placeholder': 'Type Country/State'}))
    public = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'public'}))
    profilePic = forms.ImageField(required=False, error_messages={'invalid': ("Image files only")},
                                  widget=forms.FileInput(attrs={'class': 'upload'}))

    class Meta:
        model = UserProfile
        fields = ('profilePic', 'public',)


class TripForm(forms.ModelForm):
    originText = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'id': 'origin', 'class': 'origin form-control',
               'placeholder': 'Type your origin Country/State'}))
    destinationText = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'id': 'destination', 'class': 'destination form-control',
               'placeholder': 'Type your destination Country/State'}))
    title = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'id': 'title', 'class': 'form-control', 'placeholder': 'Give your trip a title!'}))
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Trip
        # DateInput widgets
        widgets = {'startDate': DateInput(
            attrs={'class': 'start form-control', 'placeholder': 'Please select start of Trip (mm/dd/yyyy)',
                   'required': 'required'}),
            'endDate': DateInput(
                attrs={'class': 'end form-control', 'placeholder': 'Please select end of Trip (mm/dd/yyyy)',
                       'required': 'required'}),
        }
        fields = ('title', 'startDate', 'endDate')


class BlogForm(forms.ModelForm):
    title = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'id': 'title', 'class': 'form-control', 'placeholder': 'Give your blogpost a title!'}))
    content = forms.CharField(required=True, widget=forms.Textarea(
        attrs={'id': 'content', 'rows': 8, 'class': 'form-control', 'placeholder': 'Give your trip some content!'}))
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = BlogPost
        fields = ('title', 'content')


class PhotoForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ('image',)
