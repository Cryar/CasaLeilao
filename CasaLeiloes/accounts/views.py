from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, AddItemForm
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

def user_logout(request):
    logout(request)  # Logout the user
    return redirect('index')

def perfil(request):
    user = request.user
    # Add any additional context data you want to display on the dashboard
    context = {
        'user': user,
    }
    return render(request, 'perfil.html', context)

def index(request):
    items = ItemDocument.objects.all()
    context = {
        'items': items,
    }
    return render(request, 'index.html', context)
    
def watchlist(request):    
    return render(request, 'watchlist.html' )

def adminDashboard(request):
    return render(request, 'adminDashboard.html')

def add_item(request):
    if request.method == 'POST':
        form = AddItemForm(request.POST, request.FILES)  # Include request.FILES for handling images
        if form.is_valid():
            item_name = form.cleaned_data['item_name']
            starting_price = form.cleaned_data['item_price']  # Use starting_price field
            item_description = form.cleaned_data['item_description']
            item_image = form.cleaned_data['item_image']

            # Create a new ItemDocument instance
            new_item = ItemDocument(
                title=item_name,  # Assuming title corresponds to item_name
                starting_price=starting_price,
                description=item_description,
                image=item_image
            )
            new_item.save()

            return redirect('admin')  # Redirect to the admin page after adding an item
            
    else:
        form = AddItemForm()

    return render(request, 'admin.html', {'form': form})

def alter_price(request, item_id):
    item = get_object_or_404(ItemDocument, id=item_id)
    
    if request.method == 'POST':
        new_price = request.POST['new_price']
        
        # Update the item's price
        item.price = new_price
        item.save()
        
        return redirect('admin')  # Redirect back to the admin page
    
    return render(request, 'admin.html')