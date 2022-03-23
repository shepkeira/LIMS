from django.urls import path

from orders import views

app_name = "orders"

urlpatterns = [
    path('order_history/', views.order_history, name='order_history'),
    path('results/', views.results, name='results'),
    path('shopping/', views.shopping, name='shopping'),
    path('home_page/', views.home_page, name='home'),
    path('appendix_b/',views.appendix_b, name ='appendix_b'),
    path('order_page/<order_id>',views.order_page, name ='order_page'),
    path("sample/<sample_id>", views.view_sample, name="view_sample"),
    path("test_sample/<test_sample_id>", views.view_test_sample, name="view_test_sample"),
]
