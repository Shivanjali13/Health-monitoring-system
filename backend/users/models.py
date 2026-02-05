from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    
    email = models.EmailField(unique=True)
    age = models.IntegerField(null=True, blank=True)
    height = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2, help_text="Height in cm")
    #weight = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2, help_text="Weight in kg")
    gender = models.CharField(max_length=10, null=True, blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
    