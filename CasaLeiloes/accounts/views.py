from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from items.models import ItemDocument
from .models import CustomUser, Client
from items.models import ItemDocument  # Import the Item model or adjust the import based on your app structure

#changes

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Handle further logic, such as logging in the user
            return redirect('index')  # Redirect to the index page
    else:
        form = RegistrationForm()
    return render(request, 'registration/registration.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to the index page after successful login
        else:
            # Handle login failure
            pass  # You can add error messages or additional logic here
    return render(request, 'registration/login.html')

def dashboard(request):
    user = request.user
    # Add any additional context data you want to display on the dashboard
    context = {
        'user': user,
    }
    return render(request, 'dashboard.html', context)

def index(request):
    items = ItemDocument.objects.all()
    context = {
        'items': items,
    }
    return render(request, 'index.html', context)
    