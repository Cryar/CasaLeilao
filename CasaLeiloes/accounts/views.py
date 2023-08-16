from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, AddItemForm, AlterProduto
from .models import CustomUser, Client, Produtos
from django.db import connection
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
            return redirect('register')
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
    produtos = Produtos.objects.all()
    context = {
        'produtos': produtos,
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
            item_description = form.cleaned_data['item_description']
            item_image = form.cleaned_data['item_image']

            # Create a new ItemDocument instance
            new_item = Produtos(
                title=item_name,  # Assuming title corresponds to item_name
                description=item_description,
                image=item_image
            )
            new_item.save()

            return redirect('admin')  # Redirect to the admin page after adding an item
            
    else:
        form = AddItemForm()

    return render(request, 'admin.html', {'form': form})


def alter_produto(request, produto_id):
    produtos = get_object_or_404(Produtos, produto_id=produto_id)
    
    if request.method == 'POST':
        new_name= request.POST['new_name']
        new_description = request.POST['new_description']
        new_image = request.POST['new_image']
            
        with connection.cursor() as cursor:
            cursor.execute("SELECT alter_produto(%s, %s, %s, %s)",
                            [produto_id, new_name, new_description, new_image])

        return redirect('admin')  # Redirect back to the admin page

    produtos = get_object_or_404(Produtos, produto_id=produto_id)
    return render(request, 'alterproduto.html', {'produtos': produtos})