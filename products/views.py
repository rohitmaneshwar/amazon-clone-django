from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .models import Product, CartItem

def home(request):
    # Database se saare products utha lo jo available hain
    products = Product.objects.filter(is_available=True) 
    
    print("Database se kitne products aaye: ", products)
    
    # Inhe HTML file me bhej do
    context = {'products': products}
    return render(request, 'product/product_list.html', context)  

# products/views.py me sabse upar yeh naye imports daalo
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# (Tumhara pehle wala home function yahan rahega...)
# def home(request): ...

# Yeh Naya Login Function Hai
def user_login(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        
        # Check karna ki user database me hai ya nahi
        user = authenticate(request, username=u, password=p)
        
        if user is not None:
            login(request, user)  # User ko login kara do
            return redirect('home')  # Wapas homepage bhej do
        else:
            # Agar password galat ho
            return render(request, 'product/login.html', {'error': 'Galat Email ya Password! Kripya dobara check karein.'})
            
    return render(request, 'product/login.html')

# Logout karne ke liye
def user_logout(request):
    logout(request)
    return redirect('home')

# Yeh naya Signup Function hai (sabse niche daal do)
def user_signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check: Kya dono password same hain?
        if password != confirm_password:
            return render(request, 'product/signup.html', {'error': 'Passwords match nahi ho rahe hain!'})

        # Check: Kya email pehle se registered hai?
        if User.objects.filter(username=email).exists():
            return render(request, 'product/signup.html', {'error': 'Yeh Email pehle se registered hai! Pijye Sign in karein.'})

        # Naya User Create karo (Django me hum email ko hi username bana rahe hain taaki login aasan ho)
        user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
        user.save()
        
        # Account bante hi user ko automatically login karwa do
        login(request, user)
        return redirect('home')

    return render(request, 'product/signup.html')

@login_required(login_url='login')  # Agar user login nahi hai, toh use wapas login page pe bhej do
def your_account(request):
    return render(request, 'product/your_account.html')

def product_detail(request, id):
    # ID ke hisaab se product nikalenge
    product = get_object_or_404(Product, id=id)
    return render(request, 'product/product_detail.html', {'product': product})

@login_required(login_url='login')
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    # Check karo agar cart mein pehle se hai, toh quantity badhao, warna naya banao
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required(login_url='login')
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_amount = sum(item.total_price() for item in cart_items)
    total_items = sum(item.quantity for item in cart_items)
    
    context = {'cart_items': cart_items, 'total_amount': total_amount, 'total_items': total_items}
    return render(request, 'product/cart.html', context)

@login_required(login_url='login')
def checkout(request):
    # Amazon checkout me header nahi hota, isliye ise alag design karenge
    cart_items = CartItem.objects.filter(user=request.user)
    total_amount = sum(item.total_price() for item in cart_items)
    total_items = sum(item.quantity for item in cart_items)
    
    context = {'cart_items': cart_items, 'total_amount': total_amount, 'total_items': total_items}
    return render(request, 'product/checkout.html', context)

@login_required(login_url='login')
def place_order(request):
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        delivery_address = request.POST.get('delivery_address')
        
        # Agar user ne UPI/QR select kiya hai toh use QR page par bhejo
        if payment_method == 'upi':
            return redirect('upi_payment')
            
        # Agar Card ya COD select kiya hai, toh direct Order Success kar do
        else:
            # Order hone ke baad Cart ko khali kar do
            CartItem.objects.filter(user=request.user).delete()
            return redirect('order_success')
            
    return redirect('checkout')

@login_required(login_url='login')
def upi_payment(request):
    return render(request, 'product/upi_payment.html')

@login_required(login_url='login')
def order_success(request):
    # Success ke time bhi cart khali karna zaroori hai (agar UPI se wapas aaya ho)
    CartItem.objects.filter(user=request.user).delete()
    return render(request, 'product/order_success.html')



