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

        if BloodDonor.objects.filter(name = name, batch= batch).exists():
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




def adminLogin(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        if username and password:
            user = authenticate(username=username, password=password)

            if user is not None:
                auth_login(request, user)
                user.save()
                return redirect('adminApproveDonorPage')
            else:
                message = 'username & password is not correct!'
                messages.warning(request, message)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            message = 'username & password is invalid'
            messages.warning(request, message)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        message = 'Login Action cannot perform' 
        messages.warning(request, message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




def loginCheck(request):
    if request.user.is_authenticated:
        return render(request, 'AdminUser.html')
    else:
        return render(request, 'index.html')





@login_required(login_url='loginCheck')
def adminApproveDonorPage(request):
    allDonor = BloodDonor.objects.filter(status=False)
    totalApprovedDonor = BloodDonor.objects.filter(status = True).count()
    totalUnapprovedDonor = BloodDonor.objects.filter(status = False).count()
    context = {
        'allDonor': allDonor,
        'totalApprovedDonor': totalApprovedDonor,
        'totalUnapprovedDonor': totalUnapprovedDonor
    }
    return render(request, 'AdminDonorRequestList.html', context)



@login_required(login_url='loginCheck')
def adminFetchAllValidDonorPage(request):
    allDonor = BloodDonor.objects.filter(status=True)
    totalApprovedDonor = BloodDonor.objects.filter(status = True).count()
    totalUnapprovedDonor = BloodDonor.objects.filter(status = False).count()
    context = {
        'allDonor': allDonor,
        'totalApprovedDonor': totalApprovedDonor,
        'totalUnapprovedDonor': totalUnapprovedDonor
    }
    return render(request, 'AdminAllDonorFetchPage.html',context)





def logutUser(request):
    logout(request)
    return  redirect('home')




@login_required(login_url='loginCheck')
def adminAddDonor(request):
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


@login_required(login_url='loginCheck')
def adminDeleteDonor(request,id):
    try:
        instance= BloodDonor.objects.get(id=id)
        instance.delete()
        message = 'donor deleted successfully!'
        messages.success(request, message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except:
        message = 'donor delete problem!'
        messages.warning(request, message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required(login_url='loginCheck')
def adminApproveDonor(request, id):
    try:
        UpDonor = BloodDonor.objects.get(id=id)
        UpDonor.status =True
        UpDonor.save()
        message = 'Donor approved successfully'
        messages.success(request, message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except:
        message = 'donor approve problem!'
        messages.warning(request, message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
