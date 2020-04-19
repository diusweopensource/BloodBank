from django.shortcuts import render, HttpResponseRedirect
from .models import BloodDonor
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from datetime import datetime
# Create your views here.


def home(request):
    allDonor = BloodDonor.objects.filter(status = True)
    context = {
        'allDonor': allDonor
    }
    return render(request, 'index.html', context)


@csrf_exempt
def addDonor(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        blood = request.POST.get('blood')
        phone = request.POST.get('phone')
        batch = request.POST.get('batch')
        address = request.POST.get('address')

        if BloodDonor.objects.filter(name = name, blood_group = blood, batch= batch).exists():
            message = 'Donor already exists!'
            messages.info(request, message)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            bloodDonor = BloodDonor(
            name = name,
            blood_group = blood,
            phone = phone,
            batch = batch,
            address = address,
            status = True,
            created_date = datetime.now()
            )
            bloodDonor.save()
            message = 'Donor uploaded, need admin approval'
            messages.success(request, message)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        message = 'Donor upload problem!!'
        messages.warning(request, message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
