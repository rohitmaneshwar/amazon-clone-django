from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),     
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.user_signup, name='signup'),
    path('your-account/', views.your_account, name='your_account'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('upi-payment/', views.upi_payment, name='upi_payment'),
    path('order-success/', views.order_success, name='order_success'),
]