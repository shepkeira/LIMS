from django.shortcuts import render, redirect
from accounts.models import Client
from laboratoryOrders.models import Sample


# home page for laboratory workers
def home_page(request):
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")
    return render(request, 'laboratory/home_page.html')


# page listing all samples for laboratory workers
def sample_list(request):
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")
    sample_list = Sample.all_samples()
    context = {'samples': sample_list}
    return render(request, 'laboratory/sample_list.html', context)
