from admission_rawat_jalan.models import TableJadwalPraktekDokter
from admission_rawat_jalan.api import TableJadwalPraktekDokterApi
from django.core.paginator import Paginator
from user_management.models import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict


def GetAdmin(request):
    admin = TableAdmin.objects.get(pk=request.user.id)
    return admin


def LoginPage(request):
    return render(request, "frontdesk/login.html")


@login_required("", "/frontdesk/login")
def Dashboard(request):
    return render(request, "frontdesk/dashboard.html", {"admin": GetAdmin(request)})


@login_required
def Faskes(request):
    return render(request, "frontdesk/faskes.html", {"admin": GetAdmin(request)})


@login_required
def RawatJalan(request):
    return render(request, "frontdesk/rawatjalan.html", {"admin": GetAdmin(request)})


@login_required
def LogoutProses(request):
    logout(request)
    return HttpResponseRedirect('/frontdesk/login/')


@login_required
def JadwalDokter(request):
    return render(request, "frontdesk/jadwaldokter.html")


@login_required
def HalamanDokter(request):
    return render(request, "frontdesk/dokter.html")


@login_required
def DetailFaskes(request, idfaskes):
    faskes = TableFaskes.objects.get(pk=idfaskes)
    poli = TablePoli.objects.filter(id_faskes=faskes)
    admins = TableAdmin.objects.filter(id_faskes=faskes)
    print(admins)
    return render(request, "frontdesk/detailfaskes.html", {"admin": GetAdmin(request), "faskes": faskes, "poli": poli, "admins": admins})
