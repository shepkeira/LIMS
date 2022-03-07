from django.contrib.auth.forms import UserCreationForm
from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import redirect, render
from accounts.models import Client
from accounts.forms import clientForm, createUserForm
from django.contrib import messages

# view used for registration of a client or lab employee
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def registration(request):
    form = createUserForm()
    profile_form = clientForm()
    if request.method == 'POST':
        form = createUserForm(request.POST)
        profile_form = clientForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.account_number = Client.next_account_number()
            profile.save()
            messages.success(request, 'Your account has been successfully created')
            return redirect('login')
    context = {'form': form, 'profile_form': profile_form}
    return render(request, 'registration/registration.html', context)

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

