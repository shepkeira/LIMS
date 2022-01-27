from django.urls import path

from orders import views

app_name = "orders"

urlpatterns = [
    path('order_history/', views.order_history, name='order_history'),
    path('results/', views.results, name='results'),
    path('shopping/', views.shopping, name='shopping'),
    path('home_page/', views.home_page, name='home'),
    #path('orders/',views.package, name ='package'),
    path('package/',views.package, name ='package'),
    #path('sample_types/',views.sample_types, name ='sample_types'),
    path('shopping/appendix_b',views.appendix_b, name = "appendix_b"),
    #path('shopping/<int:id>/', views.shopping, name = "account_pk"),
    #path('shopping/<int:pk>/', views.shopping, name = "account_pk"),

]
