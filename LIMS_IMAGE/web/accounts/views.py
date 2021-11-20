from django.contrib.auth.forms import UserCreationForm
from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import redirect, render

from accounts.models import Client

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def login_success(request):
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")
    else:
        return redirect("accounts:employee_home_page")

def customer_home_page(request):
    return redirect("orders:home")

def employee_home_page(request):
    return redirect("laboratory:lab_home")