from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Artist

category_choices = (
    ('Painting', 'Painting'),
    ('Sculpture', 'Sculpture'),
    ('Photography', 'Photography'),
    ('Digital Art', 'Digital Art'),
    ('Mixed Media', 'Mixed Media'),
    ('Prints', 'Prints'),
    ('Drawing', 'Drawing'),
    ('Others', 'Others'),
)
gallery_choices = (
    ('Gallery 1', 'Gallery 1'),
    ('Gallery 2', 'Gallery 2'),
    ('Gallery 3', 'Gallery 3'),
    ('Gallery 4', 'Gallery 4'),
    ('Gallery 5', 'Gallery 5'),
    ('Gallery 6', 'Gallery 6'),
    ('None', 'None')
)

class ArtistProfileForm(forms.ModelForm):
    alias = forms.CharField(max_length=100, required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
    profile_image = forms.ImageField(required=True)

    class Meta:
        model = Artist
        fields = ['alias', 'description', 'profile_image']

class SellForm(forms.Form):
    art_title = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    starting_price = forms.DecimalField(max_digits=10, decimal_places=2, required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    set_duration = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    artwork_image = forms.ImageField(required=True, widget=forms.FileInput(attrs={'class': 'form-control'}))
    category = forms.ChoiceField(choices=category_choices, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    gallery = forms.ChoiceField(choices=gallery_choices, required=True, widget=forms.Select(attrs={'class': 'form-control'}))

