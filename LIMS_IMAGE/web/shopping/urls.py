from django.urls import path, include

from . import views

# Cart Urls
urlpatterns = [
    path('cart/', views.ListCart, name='list-shopingcart'),
    path('cart/<int:pk>/', views.DetailCart.as_view(), name='detail-shoppingcart'),
    path('cart/create/', views.CreateCart.as_view(), name='create-shoppingcart'),
    path('cart/<int:pk>/update/', views.Updatecart.as_view(), name='update-shoppingcart'),
    path('cart/<int:pk>/delete/', views.DeleteCart.as_view(), name='delete-shoppingcart'),
]

# CartItem Urls
urlpatterns += [
    path('cartitem/', views.ListCartItem.as_view(), name='list-cartitem'),
    path('cartitem/<int:pk>/', views.DetailCartItem.as_view(), name='detail-cartitem'),
    path('cartitem/create/', views.CreateItemCart.as_view(), name='create-cartitem'),
    path('cartitem/<int:pk>/update/', views.UpdateCartItem.as_view(), name='update-cartitem'),
    path('cartitem/<int:pk>/delete/', views.DeleteCartItem.as_view(), name='delete-cartitem'),
]