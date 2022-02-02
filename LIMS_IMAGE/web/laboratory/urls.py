from django.urls import path

from laboratory import views

app_name = "laboratory"

urlpatterns = [
    path('home_page/', views.home_page, name='lab_home'),
    path('sample_list/', views.sample_list,
         name='lab_sample_list'),  # List of all samples + search bar
]
