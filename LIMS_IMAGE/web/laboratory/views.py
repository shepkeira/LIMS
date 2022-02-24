from django.shortcuts import render, redirect
from laboratoryOrders.models import SampleInspection
from laboratoryOrders.forms import InspectionForm
from accounts.models import Client, LabWorker
from .forms import ImageForm
from src.barcoder import Barcoder
import os
from laboratoryOrders.models import Sample, LabSample, TestSample, OrderSample
from orders.models import Order
from laboratory.models import InventoryItem, Location

# home page for laboratory workers


def home_page(request):
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")
    return render(request, 'laboratory/home_page.html')

# Show samples ready to be distributed


def ready_for_distribution(request):
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")
    # Get samples that have passed inspection, but don't yet have a lab sample
    sample_results = Sample.objects.all()
    samples = []
    for s in sample_results:
        if not s.lab_samples() and s.inspection_results() == 'Valid':
            samples.append([s, s.user_side_id()])

    context = {'samples': samples}
    return render(request, 'laboratory/distribution.html', context)


def create_lab_sample(request, sample_id):
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")

    locations = Location.objects.all()
    sample = Sample.objects.filter(id=sample_id).first()

    # Form
    message = ''
    if request.method == 'POST': # Form callback with post
        results = request.POST.items()
        added = ''
        for result in results:
            if result[0] != 'csrfmiddlewaretoken' and not LabSample.objects.filter(sample=sample_id, location__code=result[1]):
                #print('Result: ' + str(result), flush=True)
                #print('Location: ' + str(Location.objects.filter(code=result[1]).first()), flush=True)
                ls = LabSample(
                    sample=Sample.objects.filter(id=sample_id).first(),
                    location=Location.objects.filter(code=result[1]).first()
                    )
                added += str(ls) + ', '
                ls.save()
                #print(added, flush=True)
                #print('Created new lab sample: ' + str(ls), flush=True)
        if added != '':
            message = 'Added lab samples: ' + added[:-2]
            print('Message: ' + message, flush=True)
            context = {'sample': sample, 'locations': locations, 'message': message}
            return render(request, 'laboratory/distribute_sample.html', context)

    context = {'sample': sample, 'locations': locations, 'message': message}
    return render(request, 'laboratory/distribute_sample.html', context)


# page listing all samples for laboratory workers


def sample_list(request):
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")
    sample_list = Sample.all_samples()
    context = {'samples': sample_list}
    return render(request, 'laboratory/sample_list.html', context)

# page listing all samples for laboratory workers


def order_list(request):
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")
    sample_list = Order.objects.all()
    context = {'samples': sample_list}
    return render(request, 'laboratory/order_list.html', context)


def validate_sample(request, sample_id):
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")
    sample = Sample.objects.filter(id=sample_id).first()
    inspection = SampleInspection.objects.filter(sample=sample).first()
    if request.method == 'POST':
        form = InspectionForm(request.POST, instance=inspection)
        message = ""
        if form.is_valid():
            inspection = form.save(commit=False)
            inspection.sample = sample
            inspection.inspector = request.user
            inspection.save()
        return view_sample(request, sample_id)
    else:
        form = InspectionForm(instance=inspection)
        return render(request, 'laboratory/validate.html', {'sample': sample, 'form': form})


def read_barcode(request):
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")
    # Process images uploaded by users
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
            id = 0
            if barcode_parts[0] == "S":
                id = barcode_parts[2]
                if len(barcode_parts) == 3:
                    # this is a sample
                    # order_id = barcode_parts[1]
                    type = "sample"
                elif len(barcode_parts) == 4:
                    # this is a lab sample
                    type = "lab_sample"
                else:
                    # this is a test sample
                    type = "test_sample"
            context = {'form': form, 'img_obj': img_obj, 'img_url': image_path_2,
                       'img_barcode': img_barcode, 'type': type, 'id': id}
            return render(request, 'laboratory/read_barcode.html', context)
    else:
        form = ImageForm()
    return render(request, 'laboratory/read_barcode.html', {'form': form})

# page listing all samples for laboratory workers


def view_barcode(request, sample_id):
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")
    # delete old files so we don't end up with a bunch in memory
    mypath = os.path.join(os.getcwd(), "static/barcodes")
    for root, dirs, files in os.walk(mypath):
        for file in files:
            if file.endswith('jpg'):
                os.remove(os.path.join(root, file))
    sample = Sample.objects.filter(id=sample_id).first()
    barcode_file_path = sample.barcode()
    barcode_file_path = os.path.join("../../../", barcode_file_path)
    context = {'barcode_file_path': barcode_file_path, "sample_id": sample_id}
    return render(request, 'laboratory/view_barcode.html', context)


def view_order(request, order_id):
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")
    order = Order.objects.filter(id=order_id).first()
    samples = OrderSample.samples_for_order(order)

    order_inspected = True
    for sample in samples:
        order_inspected = order_inspected and sample.insepcted()

    context = {'order': order, 'samples': samples,
               'order_inspected': order_inspected}
    return render(request, 'laboratory/view_order.html', context)


def view_sample(request, sample_id):
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")
    # delete old files so we don't end up with a bunch in memory
    mypath = os.path.join(os.getcwd(), "static/barcodes")
    for root, dirs, files in os.walk(mypath):
        for file in files:
            if file.endswith('jpg'):
                os.remove(os.path.join(root, file))
    sample = Sample.objects.filter(id=sample_id).first()
    inspection = sample.inspection_results()

    barcode_file_path = sample.barcode()
    barcode_file_path = os.path.join("../../../", barcode_file_path)

    lab_samples = sample.lab_samples()
    test_samples = sample.test_samples()

    order = sample.order()

    context = {'barcode_file_path': barcode_file_path, 'sample': sample, 'lab_samples': lab_samples,
               'test_samples': test_samples, 'inspection': inspection, 'order': order}
    return render(request, 'laboratory/view_sample.html', context)


def view_lab_sample(request, lab_sample_id):
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")
    # delete old files so we don't end up with a bunch in memory
    mypath = os.path.join(os.getcwd(), "static/barcodes")
    for root, dirs, files in os.walk(mypath):
        for file in files:
            if file.endswith('jpg'):
                os.remove(os.path.join(root, file))

    lab_sample = LabSample.objects.filter(id=lab_sample_id).first()

    barcode_file_path = lab_sample.barcode()
    barcode_file_path = os.path.join("../../../", barcode_file_path)

    test_samples = lab_sample.test_samples()
    sample = lab_sample.sample

    context = {'barcode_file_path': barcode_file_path,
               'lab_sample': lab_sample, 'test_samples': test_samples, 'sample': sample}
    return render(request, 'laboratory/view_lab_sample.html', context)


def view_test_sample(request, test_sample_id):
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")
    # delete old files so we don't end up with a bunch in memory
    mypath = os.path.join(os.getcwd(), "static/barcodes")
    for root, dirs, files in os.walk(mypath):
        for file in files:
            if file.endswith('jpg'):
                os.remove(os.path.join(root, file))

    test_sample = TestSample.objects.filter(id=test_sample_id).first()

    barcode_file_path = test_sample.barcode()
    barcode_file_path = os.path.join("../../../", barcode_file_path)

    lab_sample = test_sample.lab_sample_id
    sample = lab_sample.sample

    context = {'barcode_file_path': barcode_file_path,
               'lab_sample': lab_sample, 'test_sample': test_sample, 'sample': sample}
    return render(request, 'laboratory/view_test_sample.html', context)


def inventory_page(request):
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")
    inventory_list = InventoryItem.objects.all()
    context = {'inventory_list': inventory_list}
    return render(request, 'laboratory/inventory.html', context)
