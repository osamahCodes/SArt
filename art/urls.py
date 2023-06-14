"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('register/customer', views.register_customer, name='register_customer'),
    path('register/artist', views.register_artist, name='register_artist'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('login/customer', views.login_customer, name='login_customer'),
    path('login/artist', views.login_artist, name='login_artist'),
    path('create_artist_profile/', views.create_artist_profile, name='create_artist_profile'),
    path('edit_artist_profile/<int:profile_id>/', views.edit_artist_profile, name='edit_artist_profile'),
    path('delete_artist_profile/', views.delete_artist_profile, name='delete_artist_profile'),
    path('artists/', views.artists, name='artists'),
    path('artist_profile/<int:profile_id>/', views.artist_profile, name='artist_profile'),
    path('categories/', views.categories, name='categories'),
    path('galleries/', views.galleries, name='galleries'),
    path('sell/', views.sell, name='sell'),
    path('auction/', views.auction, name='auction'),
    path('auction/bid/<int:art_piece_id>/', views.auction_bid, name='auction_bid'),
    path('my_collection/', views.my_collection, name='my_collection'),
    path('my_listed_items/', views.my_listed_items, name='my_listed_items'),
    path('search/artists/', views.search_artists, name='search_artists'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)