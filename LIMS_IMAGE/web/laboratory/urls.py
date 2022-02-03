from django.urls import path

from laboratory import views

app_name = "laboratory"

urlpatterns = [
    path('home_page/', views.home_page, name='lab_home'),
    path('read_barcode/', views.read_barcode, name='read_barcode')
]
