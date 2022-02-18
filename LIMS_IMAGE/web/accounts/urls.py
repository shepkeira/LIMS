from django.urls import path

from accounts import views
from .views import SignUpView

app_name = "accounts"

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('customer_home_page/', views.customer_home_page, name='customer_home_page'),
    path('employee_home_page/', views.employee_home_page, name='employee_home_page'),
    path('login_success/', views.login_success, name='login_success'),
    path('home_page/', views.home_page, name='home_page'),

]
