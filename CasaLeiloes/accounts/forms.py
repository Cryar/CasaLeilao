from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Client
from django import forms

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name']

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()

            # Create the corresponding Client instance
            client = Client(user=user.id, username=user.username, password=user.password)
            client.save(using='mongodb')  # Save to MongoDB database
        return user

class LoginForm(AuthenticationForm):
    # No need to define fields as they are inherited from AuthenticationForm
    pass