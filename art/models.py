from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='artist_profile')
    alias = models.CharField(max_length=100)
    description = models.TextField()
    profile_image = models.ImageField(upload_to='images/')


class ArtPiece(models.Model):
    artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='art_pieces', limit_choices_to={'is_staff': True})
    title = models.CharField(max_length=100)
    start_bidding_price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DateField()
    art_piece_file = models.ImageField(upload_to='images/')
    category = models.CharField(max_length=100)
    gallery = models.CharField(max_length=100)



class Bid(models.Model):
    art_piece = models.ForeignKey(ArtPiece, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)


class Collection(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
    art_piece = models.ForeignKey(ArtPiece, on_delete=models.CASCADE, related_name='collections')
    timestamp = models.DateTimeField(auto_now_add=True)
