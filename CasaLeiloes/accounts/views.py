from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, AddItemForm, AlterProduto, BidForm, LeiloesForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .models import CustomUser, Client, Produtos, BiddingHistory, Lotes, ProdutosImage, Leiloes, Licitacoes

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
    bids = BiddingHistory.objects.all()
    images = ProdutosImage.objects.all()

    with connection.cursor() as cursor:
        # Execute the raw SQL query to fetch data from the view
        query = "SELECT * FROM product_info;"
        cursor.execute(query)
        auctions = cursor.fetchall()
        cursor.close()
    
    context = {
        'bids' : bids,
        'images' : images,
        'auctions': auctions,
    }
    return render(request, 'index.html', context)
    
def watchlist(request, auction_id): 
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
            leilao_id   = form.cleaned_data['leilao_id']
            
            item_lot_instance = Lotes.objects.get(pk=item_lot)
            
            if len(item_images) <= 3:  # Limit to 3 images
                new_item = Produtos(
                    title=item_name,
                    description=item_description,
                    lot=item_lot_instance,
                    leilao_id=leilao_id,
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

def insert_product(request):
    if request.method == 'POST':
        # Get the data for the new product from the request
        title = request.POST['item_name']
        description = request.POST['item_description']
        lot_id = int(request.POST['item_lot'])
        auction_id = int(request.POST['auction_id'])

        # Get the uploaded image file
        image = request.FILES.get('item_images')

        # Create a file system storage object
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)

        # Save the uploaded file to the media directory and get its path/URL
        if image:
            image_name = fs.save(image.name, image)
            image_path = fs.url(image_name)
        else:
            image_path = None

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT insert_product(%s, %s, %s, %s, %s)",
                [title, description, int(lot_id), int(auction_id), image_path]
            )

        return render(request,'items.html')
    
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
        auction_number = request.POST['auction_number']
        base_price = request.POST['base_price']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        minimum_increment = request.POST['minimum_increment']

        with connection.cursor() as cursor:
            cursor.execute('SELECT create_leilao(%s,%s,%s,%s,%s)', [auction_number, base_price,
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
def bid(request, bid_id):
    licitacao = get_object_or_404(Licitacoes, bid_id = bid_id)
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid_value = form.cleaned_data['bid_value']
            user = request.user  # This should now be a valid CustomUser instance
            bid_history = BiddingHistory(user=user, leilao=licitacao.auction, bid_amount=bid_value)
            bid_history.save()
            return redirect('bid', bid_id)
    else:
        form = BidForm()

    context = {'form': form, 'licitacao': licitacao}
    return render(request, 'bid.html', context)

def product_list(request):
    # You don't need to retrieve products from the model directly
    # Instead, you can fetch data from the 'public.product_info' view using raw SQL
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM public.product_info')
        rows = cursor.fetchall()

    # Define a list of dictionaries to store the fetched data
    produtos_data = []

    # Iterate through the rows and convert them to dictionaries
    for row in rows:
        produto = {
            'product_id': row[0],
            'title': row[1],
            'description': row[2],
            'created_at': row[3],
            'lot_id': row[4],
            'lot_name': row[5],
            'lot_description': row[6],
            'auction_id': row[7],
            'number_of_bids': row[8],
            'base_price': row[9],
            'auction_start': row[10],
            'auction_end': row[11],
            'minimum_increment': row[12],
            'images': row[13],
        }
        produtos_data.append(produto)

    # You can now use produtos_data to pass the data to your template
    context = {
        'produtos': produtos_data,
    }

    return render(request, 'items.html', context)

def negociacoes_list(request):
    # You don't need to retrieve products or auctions from the model directly
    # Instead, you can fetch data from the 'negociacoes' view using raw SQL
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM negociacoes')
        rows = cursor.fetchall()

    # Define a list of dictionaries to store the fetched data
    negociacoes_data = []

    # Iterate through the rows and convert them to dictionaries
    for row in rows:
        negociacao = {
            'negociacoes_id': row[0],
            'lot_id': row[1],
            'title': row[2],
            'description': row[3],
            'bid_value': row[4],
            'valor_proposto': row[5],
            'hora_inicio': row[6],
            'hora_fim': row[7],
            'auction_id': row[8],
        }
        negociacoes_data.append(negociacao)

    # You can now use negociacoes_data to pass the data to your template
    context = {
        'negociacoes': negociacoes_data,
    }

    return render(request, 'negociacoes.html', context)

def watchlist(request, auction_id):
    # Convert auction_id to an integer (assuming it's passed as a string)
    auction_id = int(auction_id)

    with connection.cursor() as cursor:
        cursor.execute("SELECT auction_id FROM accounts_leiloes WHERE auction_id = %s", [auction_id])
        result = cursor.fetchone()

        # Check if the auction with the provided ID exists in accounts_leiloes
        if result:
            # If the auction exists, call the PostgreSQL function to add it to the watchlist
            cursor.execute('SELECT add_leilao_to_watchlist(%s)', [auction_id])

    # Redirect to the index.html page (or any other page you want)
    return redirect(request, 'auction.html')

def watchlist_auctions(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM watchlist_auctions')
        auctions_data = cursor.fetchall()
    
    context = {
        'auctions_data': auctions_data,
    }
    
    return render(request, 'watchlist.html', context)