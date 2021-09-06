from builtins import print
from pasien.views import PointPasien
from django.http.response import HttpResponseRedirect
from django.contrib.auth import logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from admission_rawat_jalan.models import AdmissionRawatJalan
from user_management.models import TableFaskes, TableLogPointUser, TableRekamMedis, TableUser


def LoginPage(request):
    return render(request, "pasien/login.html", {"data": "data"})


def GetPasien(request):
    pasien = TableUser.objects.get(pk=request.user.id)
    return pasien


@login_required()
def LogoutProses(request):
    logout(request)
    return HttpResponseRedirect('/pasien/login')


@login_required
def Dashboard(request):
    JadwalAdmission = AdmissionRawatJalan.objects.filter(
        no_reg_member=request.user
    ).order_by('-id')
    userObj = TableUser.objects.get(pk=request.user.id)
    LatestPoint = TableLogPointUser.objects.filter(
        no_reg_member=userObj.no_reg_member).latest()

    paginator = Paginator(JadwalAdmission, 10)  # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "pasien/dashboard.html",  {'page_obj': page_obj, 'total_point': LatestPoint.total_point, 'pasien': GetPasien(request)})


@login_required
def FaskesPage(request):
    return render(request, "pasien/faskes.html", {"pasien": GetPasien(request)})


@login_required
def PasienProfile(request):
    pasien = TableUser.objects.get(id=request.user.id)
    lastPoint = TableLogPointUser.objects.filter(
        no_reg_member=pasien.no_reg_member).last()
    rekamMedis = TableRekamMedis.objects.filter(no_reg_member=pasien)
    return render(request, "pasien/newprofile.html", {
        "pasien": GetPasien(request),
        "data": {
            "point": {
                "total": lastPoint.total_point,
                "service": lastPoint.service,
            },
            "rekammedis": {
                "data": rekamMedis,
            },
        }})


@login_required
def PasienProfileOld(request):
    return render(request, "pasien/profile.html")


@login_required
def EditProfile(request):
    return render(request, "pasien/editprofile.html")


@login_required
def FamilyPage(request):
    return render(request, "pasien/family.html")


@login_required
def RawatJalan(request):
    return render(request, "pasien/rawatjalan.html")


@login_required
def PoliPage(request):
    idfaskes = request.GET.get("faskes")
    faskes = TableFaskes.objects.get(pk=idfaskes)
    return render(request, "pasien/polipage.html", {
        "pasien": GetPasien(request),
        "faskes": faskes,
    })


def SignUpPage(request):
    return render(request, "pasien/register.html")
