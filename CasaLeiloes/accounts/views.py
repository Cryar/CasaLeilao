from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, AddItemForm, AlterProduto, BidForm, LeiloesForm
from .models import CustomUser, Client, Produtos, BiddingHistory, Lotes, ProdutosImage, Leiloes
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

def edit_perfil(request, user_id):
    user = CustomUser.objects.get(pk=user_id)
    if request.method == 'POST':
        new_username = request.POST['new_username']
        new_email = request.POST['new_email']
        
        with connection.cursor() as cursor:
            cursor.execute('SELECT edit_user(%s,%s,%s)', [user_id, new_username, new_email])
            
        return redirect('perfil')  # Redirect to user profile page after editing
        
    context = {'user': user}
    return render(request, 'perfil_edit.html', context)


def password_change(request):
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

    with connection.cursor() as cursor:
        # Execute the raw SQL query to fetch data from the view
        query = "SELECT * FROM product_info;"
        cursor.execute(query)
        auctions = cursor.fetchall()
        cursor.close()
    

    context = {
        'produtos': produtos,
        'bids' : bids,
        'images' : images,
        'auctions':auctions,
    }
    return render(request, 'index.html', context)
    
def watchlist(request, auction_id): 
    leiloes = get_object_or_404(Leiloes, auction_id=auction_id)
    with connection.cursor() as cursor:
        cursor.execute('CALL add_to_watchlist(%s)', [auction_id])
    return redirect(request, 'auction.html' , auction_id=auction_id)

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

    context = {
            'produto': produto,
            'existing_images': existing_images,
             }
    return render(request, 'alterproduto.html', context)

def add_auction(request):
   if request.method == 'POST':
        number_of_bids = request.POST['number_of_bids']
        base_price = request.POST['base_price']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        minimum_increment = request.POST['minimum_increment']

        with connection.cursor() as cursor:
            cursor.execute('SELECT create_leilao(%s,%s,%s,%s,%s)', [number_of_bids, base_price,
                                              start_time, end_time, minimum_increment])

        return redirect('admin')  # Redirect to auctions page after inserting
   
   return render(request, 'add_auction.html')




def alter_auction(request, auction_id):
    auction = get_object_or_404(Leiloes, auction_id=auction_id) 
    if request.method == 'POST':
        number_of_bids = request.POST['number_of_bids']
        base_price = request.POST['base_price']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        minimum_increment = request.POST['minimum_increment']

        with connection.cursor() as cursor:
            cursor.execute('SELECT update_auction(%s,%s,%s,%s,%s,%s)', [auction_id, number_of_bids, base_price, start_time, end_time, minimum_increment])
            
        return redirect('admin')  # Redirect to the auctions page after updating

    return render(request, 'alter_auction.html',{'auction': auction})

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

def product_list(request):
    # Retrieve all products from the database
    produtos = Produtos.objects.all()

    # Render the products template and pass the products data
    return render(request, 'items.html', {'produtos': produtos})