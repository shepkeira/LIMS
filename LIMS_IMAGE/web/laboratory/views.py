"""
views for laboratory app
"""
import os
from django.shortcuts import render, redirect
from laboratoryOrders.models import Sample, LabSample, TestSample
from laboratoryOrders.models import OrderSample, OrderTest, TestResult, SampleInspection
from laboratoryOrders.forms import InspectionForm, TestResultForm, SampleForm
from accounts.models import Client, LabWorker, LabAdmin
from src.barcoder import Barcoder
from src.email_notification import EmailNotifications
from orders.models import Order
from laboratory.models import InventoryItem, Location, Test
from .forms import ImageForm, LocationForm, TestForm

def home_page(request):
    """
    home page for employees of the laboratory
    """
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")
    return render(request, 'laboratory/home_page.html')

def ready_for_distribution(request):
    """
    Show samples ready to be distributed
    """
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")
    # Get samples that have passed inspection, but don't yet have a lab sample
    sample_results = Sample.objects.all()
    samples = []
    for sample_result in sample_results:
        if not sample_result.lab_samples() and sample_result.inspection_results() == 'Valid':
            samples.append([sample_result, sample_result.user_side_id()])

    context = {'samples': samples}
    return render(request, 'laboratory/distribution.html', context)

def create_test_sample(request, sample_id):
    """
    create test_samples from lab_samples
    """
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")

    lab_sample = LabSample.objects.filter(id=sample_id).first()
    sample_order = OrderSample.objects.filter(sample=lab_sample.sample).first()
    order_tests = OrderTest.objects.filter(order_number=sample_order.order)
    tests = []
    for order_test in order_tests:
        test = order_test.test_id
        if test not in tests:
            tests.append(test)

    # Form
    message = ''
    if request.method == 'POST':  # Form callback with post
        results = request.POST.items()
        added = ''
        for result in results:
            test = Test.objects.filter(name=result[0]).first()
            if result[0] != 'csrfmiddlewaretoken' and not \
               TestSample.objects.filter(lab_sample_id=sample_id, test=test):
                test_sample = TestSample(
                    lab_sample_id=LabSample.objects.filter(
                        id=sample_id).first(),
                    test=Test.objects.filter(name=result[0]).first()
                )
                added += str(test_sample) + ', '
                test_sample.save()
                test_result = TestResult(
                    status='Recieved',
                    test_id=test_sample,
                )
                test_result.save()

                # Notify client and lab admins that new test sample is created
                email_notification = EmailNotifications()
                email_notification.test_sample_notif(test_sample)

        if added != '':
            message = 'Added test samples: ' + added[:-2]
            print('Message: ' + message, flush=True)
            context = {'sample': lab_sample,
                       'tests': tests, 'message': message}
            return view_lab_sample(request, sample_id)

    context = {'sample': lab_sample, 'tests': tests, 'message': message}
    return render(request, 'laboratory/analysis_sample.html', context)

def create_lab_sample(request, sample_id):
    """
    create lab_samples from samples
    """
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
            if result[0] != 'csrfmiddlewaretoken' and not \
                LabSample.objects.filter(sample=sample_id, location__code=result[1]):
                lab_sample = LabSample(
                    sample=Sample.objects.filter(id=sample_id).first(),
                    location=Location.objects.filter(code=result[1]).first()
                )
                added += str(lab_sample) + ', '
                lab_sample.save()
        if added != '':
            message = 'Added lab samples: ' + added[:-2]
            context = {'sample': sample,
                       'locations': locations, 'message': message}
            # Email client about update to their sample
            email_nofication = EmailNotifications()
            email_nofication.sample_distributed(lab_sample)

            return view_sample(request, sample_id)

    context = {'sample': sample, 'locations': locations, 'message': message}
    return render(request, 'laboratory/distribute_sample.html', context)

def sample_list(request):
    """
    list all samples (not lab or test samples)
    currently unsorted
    search by any visible field
    """
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")
    list_of_samples = Sample.all_samples()
    context = {'samples': list_of_samples}
    return render(request, 'laboratory/sample_list.html', context)

def order_list(request):
    """
    list all orders
    currently unsorted
    search by any visible field
    """
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")
    list_of_samples = Order.objects.all()
    context = {'samples': list_of_samples}
    return render(request, 'laboratory/order_list.html', context)

def create_test(request):
    """
    create new tests to perform on a test_sample
    needs unique code and name
    """
    if not request.user.is_authenticated:
        return redirect("/")
    if not LabAdmin.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.rush = False
            test.save()
        return redirect("laboratory:admin_home_page")
    else:
        form = TestForm()
        return render(request, 'laboratory/test_create.html', {'form': form})

def create_location(request):
    """
    create a new location (laboratory)
    this is where lab_samples are distributed to
    unique name and code
    """
    if not request.user.is_authenticated:
        return redirect("/")
    if not LabAdmin.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save() # test
        return redirect("laboratory:admin_home_page")
    else:
        form = LocationForm()
        return render(request, 'laboratory/lab_create.html', {'form': form})

def admin_page(request):
    """
    admin page with features unique to admin
    currently
    - create new employees
    - create new test
    - creat new location
    """
    if not request.user.is_authenticated:
        return redirect("/")
    if not LabAdmin.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")
    return render(request, 'laboratory/admin_home_page.html')

def validate_sample(request, sample_id):
    """
    validate a sample recieved in an order
    to be valid must check "Inspection Pass" for it to be valid
    recieved quantity must be filled in
    """
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")
    sample = Sample.objects.filter(id=sample_id).first()
    inspection = SampleInspection.objects.filter(sample=sample).first()
    if request.method == 'POST':
        form = InspectionForm(request.POST, instance=inspection)
        if form.is_valid():
            inspection = form.save(commit=False)
            inspection.sample = sample
            inspection.inspector = request.user
            inspection.save()

            # Send email to client when sample validated
            inspection_email_notification = EmailNotifications()
            inspection_email_notification.sample_inspected(inspection)

        return view_sample(request, sample_id)
    else:
        form = InspectionForm(instance=inspection)
        return render(request, 'laboratory/validate.html', {'sample': sample, 'form': form})

def read_barcode(request):
    """
    read a barcode uploaded
    TODO figure out how to actually scan an image instead of upload
    """
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")
    # Process images uploaded by users
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        mypath = "../../src/uploads/images"
        for root, _dirs, files in os.walk(mypath):

            for file in files:
                if file.endswith('jpg') or file.endswith('png') or file.endswith('gif'):
                    os.remove(os.path.join(root, file))
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            img_path = os.path.basename(img_obj.image.url)

            image_path_2 = os.path.join("../../src/uploads/images", img_path)
            img_barcode = Barcoder().scan_barcode(img_obj.image.url)
            barcode_type = "invalid"
            if isinstance(img_barcode, str):
                barcode_parts = img_barcode.split("-")
                id_from_barcode = 0
                print("----------")
                print(barcode_parts)
                # check which barcode type you are using by prefix S=sample I=inventory E=equipment
                if barcode_parts[0] == "S": # only barcodes for samples are implemented (S prefix)
                    if len(barcode_parts) < 3:
                        barcode_type = "invalid"
                        # not valid
                    elif len(barcode_parts) == 3:
                        # Sample barcode S-1-61
                        _order_id = barcode_parts[1]
                        id_from_barcode = barcode_parts[2]
                        barcode_type = "sample"
                    elif len(barcode_parts) == 4:
                        # Lab Sample S-1-61-A
                        _order_id = barcode_parts[1]
                        sample_id = barcode_parts[2]
                        lab_code = barcode_parts[3]
                        sample = Sample.objects.filter(id = sample_id).first()
                        lab = Location.objects.filter(code = lab_code).first()
                        id_from_barcode = LabSample.objects \
                            .filter(location = lab, sample = sample).first().id
                        barcode_type = "lab_sample"
                    elif len(barcode_parts) == 5:
                        # Test Sample S-24-22-M-10
                        _order_id = barcode_parts[1]
                        sample_id = barcode_parts[2]
                        lab_code = barcode_parts[3]
                        test_id = barcode_parts[4]
                        sample = Sample.objects.filter(id = sample_id).first()
                        lab = Location.objects.filter(code = lab_code).first()
                        lab_sample_id = LabSample.objects \
                            .filter(location = lab, sample = sample).first()
                        test = Test.objects.filter(id = test_id).first()
                        id_from_barcode = TestSample.objects \
                            .filter(lab_sample_id = lab_sample_id, test = test).first().id
                        barcode_type = "test_sample"
                    else:
                        barcode_type = "error"
                        id_from_barcode = 0
            else:
                barcode_type = "error"
                id_from_barcode = 0
            context = {'form': form, 'img_obj': img_obj, 'img_url': image_path_2,
                       'img_barcode': img_barcode, 'type': barcode_type, 'id': id_from_barcode}
            return render(request, 'laboratory/read_barcode.html', context)
    else:
        form = ImageForm()
    return render(request, 'laboratory/read_barcode.html', {'form': form})

def view_barcode(request, sample_id):
    """
    view a sample barcode for a specific sample_id
    """
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")
    # delete old files so we don't end up with a bunch in memory
    mypath = os.path.join(os.getcwd(), "static/barcodes")
    for root, _dirs, files in os.walk(mypath):
        for file in files:
            if file.endswith('jpg'):
                os.remove(os.path.join(root, file))
    sample = Sample.objects.filter(id=sample_id).first()
    barcode_file_path = sample.barcode()
    barcode_file_path = os.path.join("../../../", barcode_file_path)
    context = {'barcode_file_path': barcode_file_path, "sample_id": sample_id}
    return render(request, 'laboratory/view_barcode.html', context)

def view_order(request, order_id):
    """
    view a single order
    """
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
    """
    view a specific sample
    """
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")
    # delete old files so we don't end up with a bunch in memory
    mypath = os.path.join(os.getcwd(), "static/barcodes")
    for root, _dirs, files in os.walk(mypath):
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
    """
    view a specific lab sample
    """
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")
    # delete old files so we don't end up with a bunch in memory
    mypath = os.path.join(os.getcwd(), "static/barcodes")
    for root, _dirs, files in os.walk(mypath):
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
    """
    view a specific test sample
    """
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")
    # delete old files so we don't end up with a bunch in memory
    mypath = os.path.join(os.getcwd(), "static/barcodes")
    for root, _dirs, files in os.walk(mypath):
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
    """
    view inventory items
    """
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")
    inventory_list = InventoryItem.objects.all()
    context = {'inventory_list': inventory_list}
    return render(request, 'laboratory/inventory.html', context)

def lab_analysis(request, lab_id):
    """
    view samples in a specific lab
    """
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")

    lab = Location.objects.filter(id=lab_id).first()
    lab_samples = LabSample.objects.filter(location=lab)
    context = {'lab': lab, 'samples': lab_samples}
    return render(request, 'laboratory/lab_analysis.html', context)

def analysis(request):
    """
    view all laboratories for which you can see analysis
    """
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")

    labs = Location.objects.all()
    context = {'labs': labs}
    return render(request, 'laboratory/analysis.html', context)

def sample_analysis(request, sample_id):
    """
    analysis of a test_sample
    viewing the results of the test sample
    """
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
    """
    update the results of a test_sample
    """
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")
    sample = TestSample.objects.filter(id=sample_id).first()
    result = TestResult.objects.filter(test_id=sample).first()
    if request.method == 'POST':
        form = TestResultForm(request.POST, instance=result)
        if form.is_valid():
            result = form.save(commit=False)
            result.test_id = sample
            result.save()
            # Notify client of new test results
            result_email_notification = EmailNotifications()
            result_email_notification.test_result_notif(sample, result)

        return sample_analysis(request, sample_id)
    else:
        form = TestResultForm(instance=result)
        return render(request, 'laboratory/update_results.html', {'sample': sample, 'form': form})

def update_sample(request, sample_id):
    """
    update the details of a sample
    """
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return redirect("accounts:customer_home_page")
    sample = Sample.objects.filter(id=sample_id).first()
    # result = TestResult.objects.filter(test_id = sample).first()
    if request.method == 'POST':
        form = SampleForm(request.POST, instance=sample)
        if form.is_valid():
            sample = form.save(commit=False)
            sample.lab_personel = LabWorker.objects.filter(
                user=request.user).first()
            sample.save()
        return view_sample(request, sample_id)
    else:
        form = SampleForm(instance=sample)
        return render(request, 'laboratory/update_sample.html', {'sample': sample, 'form': form})
