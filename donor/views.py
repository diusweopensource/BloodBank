from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect,redirect
from .models import BloodDonor
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from datetime import datetime
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='loginCheck')
def home(request):
    allDonor = BloodDonor.objects.filter(status = True)
    context = {
        'allDonor': allDonor
    }
    return render(request, 'index.html', context)

def loginCheck(request):
    if request.user.is_authenticated:
        return render(request, 'admin.html')
    else:
        return render(request, 'index.html')


@login_required(login_url='loginCheck')
def adminUser2(request):
    allDonor = BloodDonor.objects.filter(status=False)
    context = {
        'allDonor': allDonor
    }
    return render(request, 'DonorReq.html', context)
def adminUser(request):
    allDonor = BloodDonor.objects.filter(status=True)

    return render(request, 'adminUser.html',{'allDonor':allDonor})

def loginpage(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        if username and password:
            user = authenticate(username=username, password=password)

            if user is not None:
                auth_login(request, user)
                user.save()
                return redirect('adminUser')
            else:
                messages.info(request, 'Username & Password is incorrect')
                return redirect('home')

def logutUser(request):
    logout(request)
    return  redirect('home')



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
            status = False,
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


def addDonor2(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        blood = request.POST.get('blood')
        phone = request.POST.get('phone')
        batch = request.POST.get('batch')
        address = request.POST.get('address')
        status =request.POST.get('status')

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

def delete(request,id):
    instance= BloodDonor.objects.get(id=id)
    instance.delete()
    return redirect('adminUser')

def update(request, id):
    UpDonor = BloodDonor.objects.get(id=id)
    UpDonor.status =True
    UpDonor.save()
    message = 'Donor Request Update'
    messages.success(request, message)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
