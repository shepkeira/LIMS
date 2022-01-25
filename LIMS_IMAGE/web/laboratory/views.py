from django.shortcuts import render, redirect
from accounts.models import Client

# Create your views here.
def home_page(request):
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")
    return render(request, 'laboratory/home_page.html')