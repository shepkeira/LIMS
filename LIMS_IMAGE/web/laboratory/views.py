from django.shortcuts import render, redirect
from laboratoryOrders.models import SampleInspection
from laboratoryOrders.forms import InspectionForm, TestResultForm, SampleForm
from accounts.models import Client, LabWorker
from .forms import ImageForm
from src.barcoder import Barcoder
import os
from laboratoryOrders.models import Sample, LabSample, TestSample, OrderSample, OrderTest, TestResult
from orders.models import Order
from laboratory.models import InventoryItem, Location, Test
from django.core.mail import send_mail

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


def create_test_sample(request, sample_id):
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")

    lab_sample = LabSample.objects.filter(id=sample_id).first()
    sample_order = OrderSample.objects.filter(sample=lab_sample.sample).first()
    order_tests = OrderTest.objects.filter(order_number=sample_order.order)
    tests = []
    for order_test in order_tests:
        tests.append(order_test.test_id)

    # Form
    message = ''
    if request.method == 'POST':  # Form callback with post
        results = request.POST.items()
        added = ''
        for result in results:
            print('Result: ' + str(result[1]), flush=True)
            print('Result: ' + str(result), flush=True)
            test = Test.objects.filter(name=result[0]).first()
            if result[0] != 'csrfmiddlewaretoken' and not TestSample.objects.filter(lab_sample_id=sample_id, test=test):
                ts = TestSample(
                    lab_sample_id=LabSample.objects.filter(
                        id=sample_id).first(),
                    test=Test.objects.filter(name=result[0]).first()
                )
                added += str(ts) + ', '
                ts.save()
                tr = TestResult(
                    status='Recieved',
                    test_id=ts,
                )
                tr.save()
        if added != '':
            message = 'Added test samples: ' + added[:-2]
            print('Message: ' + message, flush=True)
            context = {'sample': lab_sample,
                       'tests': tests, 'message': message}
            return view_lab_sample(request, sample_id)

    context = {'sample': lab_sample, 'tests': tests, 'message': message}
    return render(request, 'laboratory/analysis_sample.html', context)


def create_lab_sample(request, sample_id):
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")

    locations = Location.objects.all()
    sample = Sample.objects.filter(id=sample_id).first()

    # Form
    message = ''
    if request.method == 'POST':  # Form callback with post
        results = request.POST.items()
        added = ''
        for result in results:
            if result[0] != 'csrfmiddlewaretoken' and not LabSample.objects.filter(sample=sample_id, location__code=result[1]):
                ls = LabSample(
                    sample=Sample.objects.filter(id=sample_id).first(),
                    location=Location.objects.filter(code=result[1]).first()
                )
                added += str(ls) + ', '
                ls.save()
        if added != '':
            message = 'Added lab samples: ' + added[:-2]
            print('Message: ' + message, flush=True)
            context = {'sample': sample,
                       'locations': locations, 'message': message}
            # Email client about update to their sample
            print("Sending email to: "+OrderSample.objects.filter(sample=ls.sample).first().order.account_number.user.email, flush=True)
            send_mail(
                f'New lab sample created from your order', # Subject
                f"""
Your sample has been assigned and distributed to the {ls.location}

Please do not reply to this email.
                """, # Body
                'lims0.system@gmail.com', # From
                [OrderSample.objects.filter(sample=ls.sample).first().order.account_number.user.email], # To
                fail_silently=False, # Raise exception if failure
            )

            return view_sample(request, sample_id)

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

            # Send email to client
            send_mail(
                'Inspection Received',  # Subject
                f"""
                Dear {inspection.sample.order().account_number.user.first_name},

                Your {inspection.sample.sample_type} sample ID {inspection.sample.id} order #{inspection.sample.order().order_number} has been inspected by {inspection.inspector.first_name}.
                Results:
                    received quantity: {inspection.received_quantity}
                    Package intact: {inspection.package_intact}
                    Material intact: {inspection.material_intact}
                    Inspection pass: {inspection.inspection_pass}

                Please do not reply to this email.
                """,  # Body
                'lims0.system@gmail.com',  # From
                [inspection.sample.order().account_number.user.email],  # To
                fail_silently=False,  # Raise exception if failure
            )

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
                if file.endswith('jpg') or file.endswith('png') or file.endswith('gif'):
                    os.remove(os.path.join(root, file))
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            img_path = os.path.basename(img_obj.image.url)

            image_path_2 = os.path.join("../../src/uploads/images", img_path)
            img_barcode = Barcoder().scanBarcode(img_obj.image.url)
            if isinstance(img_barcode, str):
                barcode_parts = img_barcode.split("-")
                id = 0
                print("----------")
                print(barcode_parts)
                # check which barcode type you are using by prefix S=sample; I=inventory; E=equipment
                if barcode_parts[0] == "S": # right now we only have barcodes implemented for samples (using the S prefix)
                    if len(barcode_parts) < 3:
                        type = "invalid"
                        # not valid
                    elif len(barcode_parts) == 3:
                        # Sample barcode S-1-61
                        order_id = barcode_parts[1]
                        id = barcode_parts[2]
                        type = "sample"
                    elif len(barcode_parts) == 4:
                        # Lab Sample S-1-61-A
                        order_id = barcode_parts[1]
                        sample_id = barcode_parts[2]
                        lab_code = barcode_parts[3]
                        sample = Sample.objects.filter(id = sample_id).first()
                        lab = Location.objects.filter(code = lab_code).first()
                        id = LabSample.objects.filter(location = lab, sample = sample).first().id
                        type = "lab_sample"
                    elif len(barcode_parts) == 5:
                        # Test Sample S-24-22-M-10
                        order_id = barcode_parts[1]
                        sample_id = barcode_parts[2]
                        lab_code = barcode_parts[3]
                        test_id = barcode_parts[4]
                        sample = Sample.objects.filter(id = sample_id).first()
                        lab = Location.objects.filter(code = lab_code).first()
                        lab_sample_id = LabSample.objects.filter(location = lab, sample = sample).first()
                        test = Test.objects.filter(id = test_id).first()
                        id = TestSample.objects.filter(lab_sample_id = lab_sample_id, test = test).first().id
                        type = "test_sample"
                    else:
                        type = "error"
                        id = 0
            else:
                type = "error"
                id = 0
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


def inventory(request):
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")
    inventory_list = InventoryItem.objects.all()
    context = {'inventory_list': inventory_list}
    return render(request, 'laboratory/inventory.html', context)


def lab_analysis(request, lab_id):
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")

    lab = Location.objects.filter(id=lab_id).first()
    lab_samples = LabSample.objects.filter(location=lab)
    context = {'lab': lab, 'samples': lab_samples}
    return render(request, 'laboratory/lab_analysis.html', context)


def analysis(request):
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")

    labs = Location.objects.all()
    context = {'labs': labs}
    return render(request, 'laboratory/analysis.html', context)


def sample_analysis(request, sample_id):
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")

    test_sample = TestSample.objects.filter(id=sample_id).first()
    test_result = TestResult.objects.filter(test_id=test_sample).first()
    lab_sample = test_sample.lab_sample_id
    sample = lab_sample.sample

    context = {'lab_sample': lab_sample, 'test_sample': test_sample,
               'sample': sample, 'result': test_result}
    return render(request, 'laboratory/test_analysis.html', context)


def update_test_result(request, sample_id):
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")
    sample = TestSample.objects.filter(id=sample_id).first()
    result = TestResult.objects.filter(test_id=sample).first()
    if request.method == 'POST':
        form = TestResultForm(request.POST, instance=result)
        message = ""
        if form.is_valid():
            result = form.save(commit=False)
            result.test_id = sample
            result.save()
        return sample_analysis(request, sample_id)
    else:
        form = TestResultForm(instance=result)
        return render(request, 'laboratory/update_results.html', {'sample': sample, 'form': form})


def update_sample(request, sample_id):
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")
    sample = Sample.objects.filter(id=sample_id).first()
    # result = TestResult.objects.filter(test_id = sample).first()
    if request.method == 'POST':
        form = SampleForm(request.POST, instance=sample)
        message = ""
        if form.is_valid():
            sample = form.save(commit=False)
            sample.lab_personel = LabWorker.objects.filter(
                user=request.user).first()
            sample.save()
        return view_sample(request, sample_id)
    else:
        form = SampleForm(instance=sample)
        return render(request, 'laboratory/update_sample.html', {'sample': sample, 'form': form})
