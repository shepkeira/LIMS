from django.urls import path

from laboratory import views

app_name = "laboratory"

urlpatterns = [
    path('home_page/', views.home_page, name='lab_home'),
    path('read_barcode/', views.read_barcode, name='read_barcode'),
    path('inventory/', views.inventory, name='inventory'),
    path('validate_sample/<sample_id>/',
         views.validate_sample, name='validate_sample'),
    path('sample_list/', views.sample_list,
         name='lab_sample_list'),  # List of all samples + search bar
    path('distribution/', views.ready_for_distribution, name='distribution'),
    path('distribute_sample/<sample_id>',
         views.create_lab_sample, name='distribute_sample'),
    path('analysis_sample/<sample_id>',
         views.create_test_sample, name='analysis_sample'),
    path('order_list/', views.order_list,
         name='order_list'),  # List of all samples + search bar
    path("barcode/<sample_id>/", views.view_barcode, name="view_barcode"),
    path("order/<order_id>", views.view_order, name="view_order"),
    path("sample/<sample_id>", views.view_sample, name="view_sample"),
    path("update_sample/<sample_id>", views.update_sample, name="update_sample"),
    path("lab_sample/<lab_sample_id>",
         views.view_lab_sample, name="view_lab_sample"),
    path("test_sample/<test_sample_id>",
         views.view_test_sample, name="view_test_sample"),
    path('analysis/<lab_id>', views.lab_analysis, name="lab_analysis"),
    path('sample_analysis/<sample_id>',
         views.sample_analysis, name="sample_analysis"),
    path('analysis/', views.analysis, name='analysis'),
    path('update_test_result/<sample_id>/',
         views.update_test_result, name='update_test_result'),
]
