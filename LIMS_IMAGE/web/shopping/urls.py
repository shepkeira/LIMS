from django.urls import path, include

from . import views

app_name = "shopping"

urlpatterns = [

     path('shopping/add/<int:id>/', views.cart_add, name='cart_add'),
     path('shopping/item_clear/<int:id>/', views.item_clear, name='item_clear'),
     path('shopping/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
     path('shopping/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
     path('shopping/cart_clear/', views.cart_clear, name='cart_clear'),
     path('shopping/cart-detail/',views.cart_detail,name='cart_detail'),
]