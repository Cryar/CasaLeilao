from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Client

class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name']

class LoginForm(AuthenticationForm):
    # No need to define fields as they are inherited from AuthenticationForm
    pass