from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from . import models
from django.db.models import Max
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from decimal import Decimal

def index(request):
    return render(request, 'index.html')

def register(request):

    return render(request, 'register.html')

def register_customer(request):
    if request.method == "POST":
        username = request.POST["Username"]
        # Ensure password matches confirmation
        password = request.POST["Password"]
        

        # Attempt to create new user
        try:
            user = models.User.objects.create_user(username, username, password)
            user.save()
        except IntegrityError as e:
            print(e)
            messages.error(request, "Username already taken.")
            return render(request, "index.html")
        auth_login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "index.html")


def register_artist(request):
    if request.method == "POST":
        username = request.POST["Username"]
        # Ensure password matches confirmation
        password = request.POST["Password"]
        

        # Attempt to create new user
        try:
            user = models.User.objects.create_user(username, username, password)
            user.is_staff = True
            user.save()
        except IntegrityError as e:
            print(e)
            messages.error(request, "Username already taken.")
            return render(request, "index.html")
        auth_login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "index.html")



def login(request):
    return render(request, 'login.html')

def login_artist(request):
    if request.method == "POST":
        # Attempt to sign artist in
        username = request.POST["Username"]
        password = request.POST["Password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None and user.is_staff:
            auth_login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "Invalid username and/or password for artist login.")
            return render(request, "index.html")
    else:
        return render(request, "index.html")

def login_customer(request):
    if request.method == "POST":
        # Attempt to sign customer in
        username = request.POST["Username"]
        password = request.POST["Password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None and not user.is_staff:
            auth_login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "Invalid username and/or password for customer login.")
            return render(request, "index.html")
    else:
        return render(request, "index.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def search_artists(request):
    query = request.GET.get('query')
    artists = models.Artist.objects.filter(alias__icontains=query)
    return render(request, 'search_artists.html', {'artists': artists})

def artists(request):
    artists = models.Artist.objects.all()
    context = {'artists': artists}
    return render(request, 'artists.html', context)


def artist_profile(request, profile_id):
    artist = get_object_or_404(models.Artist, user_id=profile_id)
    user = artist.user
    art_pieces = models.ArtPiece.objects.filter(artist=user)
    context = {
        'artist': artist,
        'art_pieces': art_pieces,
    }
    return render(request, 'artist_profile.html', context)

def categories(request):
    return render(request, 'categories.html')

def galleries(request):
    return render(request, 'galleries.html')

# def sell(request):
#     return render(request, 'sell.html')
@login_required
def sell(request):
    
    if request.method == 'POST':
        form = forms.SellForm(request.POST, request.FILES)
        if form.errors:
            print(form.errors)
        if form.is_valid():
            art_piece = models.ArtPiece()
            art_piece.artist = models.User.objects.get(username=request.user, is_staff=True)
            art_piece.title = form.cleaned_data['art_title']
            art_piece.start_bidding_price = form.cleaned_data['starting_price']
            art_piece.duration = form.cleaned_data['set_duration']
            art_piece.art_piece_file = form.cleaned_data['artwork_image']
            art_piece.category = form.cleaned_data['category']
            art_piece.gallery = form.cleaned_data['gallery']
            art_piece.save()
            messages.success(request, 'Your art piece has been listed for sale.')
            return redirect('index')
    else:
        form = forms.SellForm()
        context = {
            'form': form,
        }
        return render(request, 'sell.html', context)
    return render(request, 'sell.html', {'form': form})

@login_required
def auction(request):
    art_pieces = models.ArtPiece.objects.all()
    for art_piece in art_pieces:
        highest_bid = models.Bid.objects.filter(art_piece=art_piece).aggregate(Max('amount'))
        art_piece.highest_bid = highest_bid['amount__max'] if highest_bid['amount__max'] is not None else art_piece.start_bidding_price

    return render(request, 'auction.html', {'art_pieces': art_pieces})



@login_required
def auction_bid(request, art_piece_id):
    art_piece = get_object_or_404(models.ArtPiece, pk=art_piece_id)
    if request.method == 'POST':
        bid_amount = request.POST.get('bid_amount')
        if bid_amount:
            try:
                bid_amount = Decimal(bid_amount)
                current_bid = models.Bid.objects.filter(art_piece=art_piece).order_by('-amount').first()
                if not current_bid:
                    current_bid = art_piece.start_bidding_price
                if bid_amount > current_bid.amount:
                    bid = models.Bid.objects.create(
                        art_piece=art_piece,
                        customer=request.user,
                        amount=bid_amount,
                        timestamp=timezone.now()
                    )
                    messages.success(request, f"You have successfully bid {bid.amount} on {art_piece.title}")
                else:
                    messages.warning(request, f"The bidding price must be greater than the starting price of {art_piece.start_bidding_price}")
            except ValueError:
                messages.warning(request, "Please enter a valid bid amount")
        return redirect('auction')

    current_bid = art_piece.bid_set.order_by('-amount').first()
    context = {
        'art_piece': art_piece,
        'current_bid': current_bid,
    }
    return render(request, 'auction.html', context)


def my_collection(request):
    return render(request, 'my_collection.html')

def my_listed_items(request):
    # Get all ArtPiece objects for the current user
    art_pieces = models.ArtPiece.objects.filter(artist=request.user)
    context = {'art_pieces': art_pieces}
    return render(request, 'my_listed_items.html', context)



def create_artist_profile(request):
    if request.method == 'POST':
        form = forms.ArtistProfileForm(request.POST, request.FILES)
        if form.errors:
            print(form.errors)

        if form.is_valid():
            artist = form.save(commit=False)
            artist.user = request.user
            artist.save()
            messages.success(request, 'Your artist profile has been created.')
            return redirect('index')
    else:
        form = forms.ArtistProfileForm()
    return render(request, 'create_artist_profile.html', {'form': form})

def edit_artist_profile(request, profile_id):
    profile = get_object_or_404(models.Artist, id=profile_id, user=request.user)
    if request.method == 'POST':
        form = forms.ArtistProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your artist profile has been updated.')
            return redirect('index')
    else:
        form = forms.ArtistProfileForm(instance=profile)
    return render(request, 'edit_artist_profile.html', {'form': form, 'profile': profile})

@login_required
def delete_artist_profile(request):
    try:
        artist = request.user.artist_profile
    except models.Artist.DoesNotExist:
        messages.error(request, 'You do not have an artist profile to delete.')
        return redirect('index')

    if request.method == 'POST':
        artist.delete()
        messages.success(request, 'Your artist profile has been deleted.')
        return redirect('index')

    return render(request, 'delete_artist_profile.html')