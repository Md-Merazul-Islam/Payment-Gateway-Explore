from django.db import models
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
    
# Create your models here.
class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    account_no = models.IntegerField(unique=True)
    profile_image = models.ImageField(upload_to='account/images', blank=True, null=True)
    
    def __str__(self) -> str:
        return f'{self.user.username} : {self.account_no}'