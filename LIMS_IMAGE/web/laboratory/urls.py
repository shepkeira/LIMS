from django.urls import path

from laboratory import views

app_name = "laboratory"

urlpatterns = [
    path('home_page/', views.home_page, name='lab_home'),
    path('read_barcode/', views.read_barcode, name='read_barcode'),
    path('validate_sample/<sample_id>/', views.validate_sample, name='validate_sample'),
    path('sample_list/', views.sample_list,
         name='lab_sample_list'),  # List of all samples + search bar
    path("barcode/<sample_id>/", views.view_barcode, name="view_barcode"),
    path("sample/<sample_id>", views.view_sample, name="view_sample"),
    path("lab_sample/<lab_sample_id>", views.view_lab_sample, name="view_lab_sample"),
    path("test_sample/<test_sample_id>", views.view_test_sample, name="view_test_sample")
]
