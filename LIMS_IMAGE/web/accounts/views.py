from django.contrib.auth.forms import UserCreationForm
from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import redirect, render
from accounts.models import Client

# view used for registration of a client or lab employee
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

# this function is used to rediect a user after login to the correct home_page
def login_success(request): # TODO this can be renamed
    """
    If user is authenticated, redirect to their homepage - client user to client home page, employee user to employee home page
    """
    if request.user.is_authenticated:
        if Client.objects.filter(user=request.user):
            return redirect("accounts:customer_home_page")
        else:
            return redirect("accounts:employee_home_page")
    else:
        return redirect("/")

# this function is for the customer home page, which if found in the orders app
def customer_home_page(request):
    return redirect("orders:home")

# this function is for the employee home page, which is found in the laboratory app
def employee_home_page(request):
    return redirect("laboratory:lab_home")

# this funciton is used to redirect someone to the correct home page based on if they are login in and who they are login as
def home_page(request):
    if request.user.is_authenticated:
        if Client.objects.filter(user=request.user):
            return redirect("accounts:customer_home_page")
        else:
            return redirect("accounts:employee_home_page")
    return render(request,'home.html')

