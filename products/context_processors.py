from .models import CartItem

def cart_item_count(request):
    count = 0
    # Agar user login hai, toh uske cart items gin lo
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        # Saare items ki quantity ko jod lo
        count = sum(item.quantity for item in cart_items)
    
    return {'cart_count': count}