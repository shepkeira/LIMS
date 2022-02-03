from django.shortcuts import render, redirect
from accounts.models import Client
from .forms import ImageForm
from src.barcoder import Barcoder
import os
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

def read_barcode(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        mypath = "../../src/uploads/images"
        for root, dirs, files in os.walk(mypath):
            for file in files:
                if file.endswith('jpg'):
                    os.remove(os.path.join(root, file))
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            img_path = os.path.basename(img_obj.image.url)
            
            image_path_2 = os.path.join("../../src/uploads/images", img_path)
            img_barcode = Barcoder().scanBarcode(img_obj.image.url)
            barcode_parts = img_barcode.split("-")
            type = barcode_parts[0]
            id = 0
            if barcode_parts[0] == "S":
                # this is a sample
                # order_id = barcode_parts[1]
                id = barcode_parts[2]
            return render(request, 'laboratory/read_barcode.html', {'form': form, 'img_obj': img_obj, 'img_url': image_path_2, 'img_barcode': img_barcode, 'type': type, 'id': id})
    else:
        form = ImageForm()
    return render(request, 'laboratory/read_barcode.html', {'form': form})

    
