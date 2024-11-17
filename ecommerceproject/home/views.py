from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages import get_messages
from .models import Product, Cart, Contact

# Create your views here.
def base(request):
    return render(request, 'base.html')

def home(request):
    products = Product.objects.all()
    print(products)
    return render(request, 'home.html', {'pdts': products})

def search_products(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(desc__icontains=query)
        )
    else:
        products = Product.objects.none()
    
    context = {
        'pdts': products,
        'query': query,
    }
    return render(request, 'search_results.html', context)

def category_view(request, category_name):
    products = Product.objects.filter(category__iexact=category_name)
    print(f"Category: {category_name}")
    print(f"Products found: {products.count()}")
    
    context = {
        'pdts': products,
        'category': category_name
    }
    return render(request, 'category.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        department = request.POST.get('department')
        message = request.POST.get('message')

        Contact.objects.create(
            name=name,
            email=email,
            department=department,
            message=message
        )
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')

    return render(request, 'contact.html')

def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Validation
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid email address')
            return redirect('signup')

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')

        if len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long')
            return redirect('signup')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('signup')

        # Create user
        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password1,
                first_name=name
            )
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
        except Exception as e:
            messages.error(request, 'An error occurred during registration')
            return redirect('signup')

    return render(request, 'signup.html')

def user_login(request):
    # Clear any existing messages when loading the login page
    storage = get_messages(request)
    for message in storage:
        pass  # This will clear all existing messages
        
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password')
                return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password')
            return redirect('login')
    
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('home')

@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)
        # Check if product already in cart
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product
        )
        
        if not created:
            # Product already in cart, increment quantity
            cart_item.quantity += 1
            cart_item.save()
            messages.info(request, f'Increased {product.name} quantity in cart')
        else:
            messages.success(request, f'Added {product.name} to cart')
        
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    return redirect('home')

@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total
    }
    return render(request, 'cart.html', context)

@login_required
def update_cart(request, item_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item = Cart.objects.get(id=item_id, user=request.user)
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated successfully')
        else:
            cart_item.delete()
            messages.info(request, 'Item removed from cart')
            
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        cart_item = Cart.objects.get(id=item_id, user=request.user)
        cart_item.delete()
        messages.success(request, 'Item removed from cart')
    return redirect('cart')

