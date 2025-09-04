from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
#accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        max_length=150,
        help_text="Only unique username required."
    )


    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'gender', 'password1', 'password2')


class EditProfileForm(forms.ModelForm):
    username = forms.CharField(
        required=True,
        max_length=150,
        validators=[],
        help_text="Only unique username required."
    )
    class Meta:
        model = User
        fields = ('profile_pic','username','email','phone_number','bio','birthdate','gender')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'birthdate': forms.DateInput(attrs={'type': 'date'}),

        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username or Phone", max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
