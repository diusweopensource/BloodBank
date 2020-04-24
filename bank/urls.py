"""bank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from donor import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('addDonor', views.addDonor, name='addDonor'),
    path('adminLogin', views.adminLogin, name='adminLogin'),
    path('loginCheck', views.loginCheck, name='loginCheck'),
    path('adminApproveDonorPage', views.adminApproveDonorPage, name='adminApproveDonorPage'),
    path('adminFetchAllValidDonorPage', views.adminFetchAllValidDonorPage, name='adminFetchAllValidDonorPage'),
    path('logutUser', views.logutUser, name='logutUser'),
    path('adminDeleteDonor/<int:id>', views.adminDeleteDonor, name='adminDeleteDonor'),
    path('adminApproveDonor/<int:id>', views.adminApproveDonor, name='adminApproveDonor'),
    path('adminAddDonor', views.adminAddDonor, name='adminAddDonor'),
]
