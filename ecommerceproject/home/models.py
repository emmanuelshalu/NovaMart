from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    # Define fields for the category model
    name = models.CharField(max_length=50)
    desc = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='categories/images/')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    # Define fields for the product model
    name = models.CharField(max_length=100)
    desc = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    category = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s cart - {self.product.name}"

    @property
    def total_price(self):
        return self.quantity * self.product.price

class Contact(models.Model):
    DEPARTMENT_CHOICES = [
        ('Sales', 'Sales'),
        ('Customer Support', 'Customer Support'),
        ('Technical Support', 'Technical Support'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)
    message = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name} - {self.department}"

    class Meta:
        ordering = ['-date_submitted']  # Most recent messages first

