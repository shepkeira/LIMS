from django.contrib.auth.forms import UserCreationForm
from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import redirect, render
from accounts.models import Client, LabWorker, LabAdmin
from accounts.forms import clientForm, createUserForm, workerForm, adminForm
from django.contrib import messages
from django.contrib.auth.models import Group

# view used for registration of a client or lab employee
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def admin_registration(request):
    if not request.user.is_authenticated:
        return redirect("/")
    if not (LabAdmin.objects.filter(user=request.user) or request.user.is_superuser):
        return redirect(home_page)
    form = createUserForm()
    admin_form = adminForm()
    if request.method == 'POST':
        form = createUserForm(request.POST)
        admin_form = adminForm(request.POST)
        if form.is_valid() and admin_form.is_valid():
            user = form.save()
            profile = admin_form.save(commit=False)
            profile.user = user
            profile.save()
            group = Group.objects.get(name='Lab admins') 
            group.user_set.add(user)
            user.is_staff=True 
            user.save()
            messages.success(request, 'Your account has been successfully created')
            return redirect('login')
    context = {'form': form, 'profile_form': admin_form}
    return render(request, 'registration/registration.html', context)

def employee_registration(request):
    if not request.user.is_authenticated:
        return redirect("/")
    if not (LabAdmin.objects.filter(user=request.user) or request.user.is_superuser):
        return redirect(home_page)
    form = createUserForm()
    worker_form = workerForm()
    if request.method == 'POST':
        form = createUserForm(request.POST)
        worker_form = workerForm(request.POST)
        if form.is_valid() and worker_form.is_valid():
            user = form.save()
            profile = worker_form.save(commit=False)
            profile.user = user
            profile.save()
            group = Group.objects.get(name='Lab workers')
            group.user_set.add(user)
            user.is_staff=True
            user.save()
            messages.success(request, 'Your account has been successfully created')
            return redirect('login')
    context = {'form': form, 'profile_form': worker_form}
    return render(request, 'registration/registration.html', context)


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
            group = Group.objects.get(name='Clients')
            group.user_set.add(user)
            user.save()
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

