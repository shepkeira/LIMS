"""
urls for accounts pages
"""
from django.urls import path

from accounts import views

app_name = "accounts"

urlpatterns = [
    path('customer_home_page/', views.customer_home_page, name='customer_home_page'),
    path('employee_home_page/', views.employee_home_page, name='employee_home_page'),
    path('login_success/', views.login_success, name='login_success'),
    path('home_page/', views.home_page, name='home_page'),
    path('registration/', views.registration, name='registration'),
    path('admin_registration/', views.admin_registration, name='admin_registration'),
    path('employee_registration/', views.employee_registration, name='employee_registration'),
]
