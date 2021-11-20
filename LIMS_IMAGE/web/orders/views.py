from django.shortcuts import render

# Create your views here.
def home_page(request):
    return render(request, 'orders/home_page.html')

def order_history(request):
    return render(request, 'orders/order_history.html')

def results(request):
    return render(request, 'orders/results.html')

def shopping(request):
    return render(request, 'orders/shopping.html')