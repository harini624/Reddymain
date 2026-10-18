
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Properties


class RegisterForm(UserCreationForm):

    email = forms.EmailField(required=True)

    first_name = forms.CharField(
        max_length=100,
        required=True
    )

    last_name = forms.CharField(
        max_length=100,
        required=False
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2'
        ]

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'This username is already taken. Please choose another.'
            )

        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'This email is already registered.'
            )

        return email

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()

        return user


class PropertyForm(forms.ModelForm):

    class Meta:
        model = Properties

        fields = [
            'title',
            'property_type',
            'purpose',
            'location',
            'city',
            'price',
            'bhk',
            'bathrooms',
            'area',
            'description',
            'house_image',
            'is_featured',
        ]

        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': 'Enter property title'}
            ),

            'location': forms.TextInput(
                attrs={'placeholder': 'Locality / Area'}
            ),

            'city': forms.TextInput(
                attrs={'placeholder': 'City'}
            ),

            'price': forms.NumberInput(
                attrs={'placeholder': 'Property price'}
            ),

            'bhk': forms.NumberInput(
                attrs={'placeholder': 'Bedrooms / BHK'}
            ),

            'bathrooms': forms.NumberInput(
                attrs={'placeholder': 'Bathrooms'}
            ),

            'area': forms.NumberInput(
                attrs={'placeholder': 'Area in sq.ft'}
            ),

            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Describe your property...',
                    'rows': 5
                }
            ),
        }
