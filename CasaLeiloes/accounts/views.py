from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, AddItemForm, AlterProduto, BidForm
from .models import CustomUser, Client, Produtos, BiddingHistory, Lotes, ProdutosImage
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
    bids = BiddingHistory.objects.all()
    images = ProdutosImage.objects.all()
    context = {
        'produtos': produtos,
        'bids' : bids,
        'images' : images,
    }
    return render(request, 'index.html', context)
    
def watchlist(request):    
    return render(request, 'watchlist.html' )

def adminDashboard(request):
    return render(request, 'adminDashboard.html')

def add_item(request):
    if request.method == 'POST':
        form = AddItemForm(request.POST, request.FILES)
        if form.is_valid():
            item_name = form.cleaned_data['item_name']
            item_description = form.cleaned_data['item_description']
            item_lot = form.cleaned_data['item_lot']
            item_images = form.cleaned_data['item_images']  # Get list of uploaded images
            
            item_lot_instance = Lotes.objects.get(pk=item_lot)
            
            if len(item_images) <= 3:  # Limit to 3 images
                new_item = Produtos(
                    title=item_name,
                    description=item_description,
                    lot=item_lot_instance,
                )
                new_item.save()

                # Create ProdutosImage instances and associate them with the new product
                for image in item_images:
                    ProdutosImage.objects.create(produto=new_item, image=image)

                return redirect('admin')  # Redirect to the admin page after adding an item
            else:
                error_message = "You can only upload up to 3 images."
        else:
            error_message = "Form is not valid."
    else:
        form = AddItemForm()
        error_message = ""

    return render(request, 'admin.html', {'form': form, 'error_message': error_message})

def alter_produto(request, product_id):
    produto = get_object_or_404(Produtos, product_id=product_id)
    existing_images = ProdutosImage.objects.filter(produto=produto)  # Fetch existing images
    
    if request.method == 'POST':
        new_name = request.POST['new_name']
        new_description = request.POST['new_description']
        new_lot = request.POST['new_lot']
        new_image = request.POST['new_image']  # Get a list of uploaded images
        deleted_images = request.POST['deleted_images'] # Get a list of images to delete
        
        if not deleted_images:
             deleted_images = []

        with connection.cursor() as cursor:
            cursor.execute(
                "CALL update_product(%s,%s,%s,%s,%s,%s)", 
                [product_id, new_name, new_description, new_image, deleted_images, new_lot])

        return redirect('admin')  # Redirect back to the admin page

    return render(request, 'alterproduto.html', {'produtos': produto, 'existing_images': existing_images})

from django.contrib.auth.decorators import login_required

@login_required
def bid(request, product_id):
    produto = get_object_or_404(Produtos, product_id=product_id)
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid_amount = form.cleaned_data['bid_amount']
            user = request.user  # This should now be a valid CustomUser instance
            bid_history = BiddingHistory(user=user, item=produto, bid_amount=bid_amount)
            bid_history.save()
            return redirect('bid', product_id=product_id)
    else:
        form = BidForm()

    context = {'form': form, 'produto': produto}
    return render(request, 'bid.html', context)