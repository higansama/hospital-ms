from django.shortcuts import render
from .models import *
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from user_management.api.dokter_api import *
from user_management.api.user_api import *
import datetime
# from dateutil.parser import parse

from goldenhour.utils.my_custom_exception_handler import (
    BaseCustomException,
    InvalidUsage,
)
from goldenhour import helpers
from django.db.models import Sum

# Create your views here.


def Test(request):
    datas = TableProvinsi.objects.all()
    result = ""
    for data in datas:
        result += data.provinsi + "<br>"
    return HttpResponse(result)


@csrf_exempt
def PerawatRegister(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        email = request.POST.get("email", "")
        no_ktp = request.POST.get("no_ktp", "")
        no_telepon = request.POST.get("no_telepon", "")
        id_faskes = request.POST.get("id_faskes", "")
        id_poli = request.POST.get("id_poli", "")
        is_staff = True
        faskes = TableFaskes.objects.get(pk=id_faskes)
        poli = TablePoli.objects.get(pk=id_poli)
        nama = first_name + " " + last_name
        no_reg_perawat = RegistrationCodeGenerator(
            4, TablePerawat.objects.filter(jenis_anggota=4).count(), faskes.faskes
        )
        try:
            dokter = TablePerawat.objects.create(
                username=username,
                password=make_password(password),
                first_name=first_name,
                last_name=last_name,
                email=email,
                no_ktp=no_ktp,
                no_telepon=no_telepon,
                is_staff=is_staff,
                id_faskes=faskes,
                id_poli=poli,
                jenis_anggota=3,
                no_reg_perawat=no_reg_perawat,
                nama=nama,
            ).save()
            return JsonResponse({"message": "sukses", "no_reg_perawat": no_reg_perawat})
        except Exception as e:
            return HttpResponse(e)
    if request.method == "GET":
        qs = TablePerawat.objects.all()
        qsdata = PerawatApi(qs, many=True)
        return JsonResponse(
            {
                "code": 200,
                "message": "success",
                "data": qsdata.data,
            }
        )


@csrf_exempt
def DocterRegister(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        email = request.POST.get("email", "")
        no_ktp = request.POST.get("no_ktp", "")
        no_telepon = request.POST.get("no_telepon", "")
        id_faskes = request.POST.get("id_faskes", "")
        id_poli = request.POST.get("id_poli", "")
        is_staff = True
        faskes = TableFaskes.objects.get(pk=id_faskes)
        poli = TablePoli.objects.get(pk=id_poli)
        nama = first_name + " " + last_name
        no_reg_dokter = RegistrationCodeGenerator(
            2, TableDokter.objects.filter(jenis_anggota=2).count(), faskes.faskes
        )
        try:
            dokter = TableDokter.objects.create(
                username=username,
                password=make_password(password),
                first_name=first_name,
                last_name=last_name,
                email=email,
                no_ktp=no_ktp,
                no_telepon=no_telepon,
                is_staff=is_staff,
                id_faskes=faskes,
                id_poli=poli,
                jenis_anggota=3,
                no_reg_dokter=no_reg_dokter,
                nama=nama,
            ).save()
            return JsonResponse({"message": "sukses", "no_reg_dokter": no_reg_dokter})
        except Exception as e:
            return HttpResponse(e)

    if request.method == "GET":
        qs = TableDokter.objects.all()
        qsdata = DokterApi(qs, many=True)
        return JsonResponse(
            {
                "code": 200,
                "message": "success",
                "data": qsdata.data,
            }
        )


@csrf_exempt
def StaffRegister(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        email = request.POST.get("email", "")
        no_ktp = request.POST.get("no_ktp", "")
        no_telepon = request.POST.get("no_telepon", "")
        id_divisi = request.POST.get("id_divisi", "")
        id_faskes = request.POST.get("id_faskes", "")
        is_staff = True
        faskes = TableFaskes.objects.get(pk=id_faskes)
        divisi_id = TableDivisi.objects.get(pk=id_divisi)
        nama = first_name + " " + last_name
        no_reg_admin = RegistrationCodeGenerator(
            1, TableAdmin.objects.filter(jenis_anggota=1).count(), faskes.faskes
        )
        try:
            dokter = TableAdmin.objects.create(
                username=username,
                password=make_password(password),
                first_name=first_name,
                last_name=last_name,
                email=email,
                no_ktp=no_ktp,
                no_telepon=no_telepon,
                is_staff=is_staff,
                jenis_anggota=1,
                no_reg_admin=no_reg_admin,
                nama=nama,
                divisi_id=divisi_id,
                id_faskes=faskes,
            ).save()

        except Exception as e:
            return HttpResponse(e)
        return JsonResponse({"message": "success"})

    if request.method == "GET":
        qs = TableAdmin.objects.all()
        qsdata = AdminApi(qs, many=True)
        return JsonResponse(qsdata.data, safe=False)


@csrf_exempt
def UserRegister(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = make_password(request.POST.get("password", ""))
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        email = request.POST.get("email", "")
        no_ktp = request.POST.get("no_ktp", "")
        no_telepon = request.POST.get("no_telepon", "")
        no_ponsel = request.POST.get("no_ponsel", "")
        profesi = request.POST.get("profesi", "")
        tingkat_pendidikan = request.POST.get("tingkat_pendidikan", "")
        kodepos_utama = request.POST.get("kodepos_utama", "")
        kodepos_domisili = request.POST.get("kodepos_domisili", "")
        alamat_domisili = request.POST.get("alamat_domisili", "")
        alamat_utama = request.POST.get("alamat_utama", "")
        kelurahan_utama = TableKelurahan.objects.get(
            pk=request.POST.get("kelurahan_utama", "")
        )
        kecamatan_utama = TableKecamatan.objects.get(
            pk=request.POST.get("kecamatan_utama", "")
        )
        kota_utama = TableKota.objects.get(pk=request.POST.get("kota_utama", ""))
        provinsi_utama = TableProvinsi.objects.get(
            pk=request.POST.get("provinsi_utama", "")
        )
        kelurahan_domisili = TableKelurahan.objects.get(
            pk=request.POST.get("kelurahan_domisili", "")
        )
        kecamatan_domisili = TableKecamatan.objects.get(
            pk=request.POST.get("kecamatan_domisili", "")
        )
        kota_domisili = TableKota.objects.get(pk=request.POST.get("kota_domisili", ""))
        provinsi_domisili = TableProvinsi.objects.get(
            pk=request.POST.get("provinsi_domisili", "")
        )
        tempat_lahir = request.POST.get("tempat_lahir", "")
        tgl_lahir = request.POST.get("tgl_lahir", "")
        jenis_kelamin = request.POST.get("jenis_kelamin", "")
        no_asuransi = request.POST.get("no_asuransi", "")
        status_keanggotaan = request.POST.get("status_keanggotaan", "")
        foto_identitas = request.POST.get("foto_identitas", "")
        jenis_anggota = 3
        nama = first_name + " " + last_name
        no_reg_member = RegistrationPasienGenerator(3, TableUser.objects.all())
        try:
            pasien = TableUser.objects.create(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
                no_ktp=no_ktp,
                no_telepon=no_telepon,
                no_ponsel=no_ponsel,
                profesi=profesi,
                tingkat_pendidikan=tingkat_pendidikan,
                kodepos_utama=kodepos_utama,
                kodepos_domisili=kodepos_domisili,
                alamat_domisili=alamat_domisili,
                alamat_utama=alamat_utama,
                kelurahan_utama=kelurahan_utama,
                kecamatan_utama=kecamatan_utama,
                kota_utama=kota_utama,
                provinsi_utama=provinsi_utama,
                kelurahan_domisili=kelurahan_domisili,
                kecamatan_domisili=kecamatan_domisili,
                kota_domisili=kota_domisili,
                provinsi_domisili=provinsi_domisili,
                tempat_lahir=tempat_lahir,
                # tgl_lahir = parse(tgl_lahir),
                jenis_kelamin=jenis_kelamin,
                no_asuransi=no_asuransi,
                status_keanggotaan=status_keanggotaan,
                foto_identitas=foto_identitas,
                jenis_anggota=jenis_anggota,
                nama=nama,
                no_reg_member=no_reg_member,
                inisial=helpers.abbreviator(nama),
            ).save()
            print("pasien ->", TableUser.objects.get(username=user_management))
            # TableRekamMedis.objects.create(
            #     no_rekam_medis="",
            #     tindakan_pengobatan="",
            #     diagnosa="",
            #     no_reg_member=,
            #     no_reg_dokter=None,
            # ).save()
            return JsonResponse({"message": "sukses", "no_reg_member": no_reg_member})
        except Exception as e:
            return HttpResponse(e)
    if request.method == "GET":
        qs = TableUser.objects.all()
        qsdata = UserSerializer(qs, many=True)
        return JsonResponse(qsdata.data, safe=False)

@csrf_exempt
def Family(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = make_password(request.POST.get("password", ""))
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        email = request.POST.get("email", "")
        no_ktp = request.POST.get("no_ktp", "")
        no_telepon = request.POST.get("no_telepon", "")
        no_ponsel = request.POST.get("no_ponsel", "")
        profesi = request.POST.get("profesi", "")
        tingkat_pendidikan = request.POST.get("tingkat_pendidikan", "")
        kodepos_utama = request.POST.get("kodepos_utama", "")
        kodepos_domisili = request.POST.get("kodepos_domisili", "")
        alamat_domisili = request.POST.get("alamat_domisili", "")
        alamat_utama = request.POST.get("alamat_utama", "")
        kelurahan_utama = TableKelurahan.objects.get(
            pk=request.POST.get("kelurahan_utama", "")
        )
        kecamatan_utama = TableKecamatan.objects.get(
            pk=request.POST.get("kecamatan_utama", "")
        )
        kota_utama = TableKota.objects.get(pk=request.POST.get("kota_utama", ""))
        provinsi_utama = TableProvinsi.objects.get(
            pk=request.POST.get("provinsi_utama", "")
        )
        kelurahan_domisili = TableKelurahan.objects.get(
            pk=request.POST.get("kelurahan_domisili", "")
        )
        kecamatan_domisili = TableKecamatan.objects.get(
            pk=request.POST.get("kecamatan_domisili", "")
        )
        kota_domisili = TableKota.objects.get(pk=request.POST.get("kota_domisili", ""))
        provinsi_domisili = TableProvinsi.objects.get(
            pk=request.POST.get("provinsi_domisili", "")
        )
        tempat_lahir = request.POST.get("tempat_lahir", "")
        tgl_lahir = request.POST.get("tgl_lahir", "")
        jenis_kelamin = request.POST.get("jenis_kelamin", "")
        no_asuransi = request.POST.get("no_asuransi", "")
        status_keluarga = request.POST.get("status_keluarga", "")
        status_keanggotaan = request.POST.get("status_keanggotaan", "")
        foto_identitas = request.POST.get("foto_identitas", "")
        jenis_anggota = 4
        nama_keluarga = first_name + " " + last_name
        parent = request.POST.get("parent")
        no_reg_family = RegistrationCodeGeneratorFamily(TableUserKeluarga.objects.filter(parent=parent).count())
        try:
            pasien = TableUserKeluarga.objects.create(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
                no_ktp=no_ktp,
                no_telepon=no_telepon,
                no_ponsel=no_ponsel,
                profesi=profesi,
                tingkat_pendidikan=tingkat_pendidikan,
                kodepos_utama=kodepos_utama,
                kodepos_domisili=kodepos_domisili,
                alamat_domisili=alamat_domisili,
                alamat_utama=alamat_utama,
                kelurahan_utama=kelurahan_utama,
                kecamatan_utama=kecamatan_utama,
                kota_utama=kota_utama,
                provinsi_utama=provinsi_utama,
                kelurahan_domisili=kelurahan_domisili,
                kecamatan_domisili=kecamatan_domisili,
                kota_domisili=kota_domisili,
                provinsi_domisili=provinsi_domisili,
                tempat_lahir=tempat_lahir,
                # tgl_lahir = parse(tgl_lahir),
                jenis_kelamin=jenis_kelamin,
                no_asuransi=no_asuransi,
                status_keanggotaan=status_keanggotaan,
                foto_identitas=foto_identitas,
                jenis_anggota=jenis_anggota,
                nama_keluarga=nama_keluarga,
                parent=parent,
                no_reg_family=no_reg_family
            ).save()
            TableRekamMedis.objects.create(
                no_rekam_medis="",
                tindakan_pengobatan="",
                diagnosa="",
                no_reg_member=no_reg_family,
            ).save()
            return JsonResponse({"message": "sukses", "no_reg_family": no_reg_family})
        except Exception as e:
            return HttpResponse(e)
    if request.method == "GET":
        qs = TableUser.objects.all()
        qsdata = UserSerializer(qs, many=True)
        return JsonResponse(qsdata.data, safe=False)

def FamilyList(request, tahun, bulan, tanggal, index):
    noreg = tahun + "/" + bulan + "/" + tanggal + "/" + index
    try:
        qs = TableUserKeluarga.objects.filter(parent=noreg)
        serialData = TableKeluargaApi(qs, many=True)
        return JsonResponse(serialData.data, safe=False)
    except Exception as e:
        return HttpResponse(str(e))
    


@csrf_exempt
def PointUser(request, tahun, bulan, tanggal, index):
    noreg = tahun + "/" + bulan + "/" + tanggal + "/" + index
    qs = TableLogPointUser.objects.filter(no_reg_member=noreg)
    if request.method == "GET":
        try:
            data = TableLogPointUserApi(qs, many=True)
            return JsonResponse(data.data, safe=False)
        except Exception as e:
            return HttpResponse(str(e))
    if request.method == "POST":
        GetPoint = request.POST.get("point")
        activity = request.POST.get("activity")
        tp = int(GetPoint)
        for ob in qs:
            tp += ob.point
        try:
            TableLogPointUser.objects.create(
                point=GetPoint,
                activity=activity,
                total_point=tp,
                no_reg_member=noreg,
            ).save()
            return JsonResponse({"message": "success"})
        except Exception as e:
            return HttpResponse(str(e))


@csrf_exempt
def RekamMedis(request, tahun, bulan, tanggal, index):
    noreg = tahun + "/" + bulan + "/" + tanggal + "/" + index
    if request.method == "GET":
        try:
            qs = TableRekamMedis.objects.all().filter(no_reg_member=noreg)
            data = TableRekamMedisApi(qs, many=True)
            return JsonResponse(data.data, safe=False)
        except Exception as e:
            return HttpResponse(str(e))


# @csrf_exempt
# def SaveRekamMedis(request):
#     if request.method == "POST":
#         no_reg_member = request.POST.get("no_reg_member", "")
#         inisial = TableUser.objects.get(no_reg_member=no_reg_member).nama
#         # cek if initial tersebut sudah masuk ke table rekam medis atau belum start
#         register = TableRekamMedis.objects.filter(no_rekam_medis__contains=inisial)
#         status = False
#         jumlah = 0
#         if len(register) != 0:
#             status = True
        
#         # cek if initial tersebut sudah masuk ke table rekam medis atau belum stop
#         no_rekam_medis = helpers.RekamMedisGenerator(status, register.count(), inisial)
#         tindakan_pengobatan = request.POST.get("tindakan")
#         diagnosa = request.POST.get("diagnosa", "")
#         id_dokter = request.POST.get(
#             "id_dokter", ""
#         )  # harusnya ini bisa diganti dari id token
#         # tgl_pengobatan = request.POST.get("tgl_pengobatan", "")
#         try:
#             rekamMedis = TableRekamMedis.objects.create(
#                 tindakan_pengobatan=tindakan_pengobatan,
#                 diagnosa=diagnosa,
#                 id_dokter=id_dokter,
#                 no_rekam_medis=no_rekam_medis,
#                 # tgl_pengobatan=tgl_pengobatan,
#                 no_reg_member=no_reg_member,
#             ).save()
#             return JsonResponse({"message": "success"})
#         except Exception as e:
#             return HttpResponse(str(e))


@csrf_exempt
def DocterPoint(request, nama_faskes, tahun, bulan, tgl, no_urut):
    kodereg = nama_faskes + "/dokter/" + tahun + "/" + bulan + "/" + tgl + "/" + no_urut
    Dokter = TableLogPointDokter.objects.filter(no_reg_dokter=kodereg)
    if request.method == "GET":
        try:
            qsData = TableLogPointDokterApi(Dokter, many=True)
            return JsonResponse(qsData.data, safe=False)
        except Exception as e:
            return HttpResponse(str(e))

    if request.method == "POST":
        pointget = request.POST.get("get_point", "0")
        minuspoint = request.POST.get("minus_point", "0")
        servicedid = request.POST.get("service")
        lastpoint = 0
        if  len(Dokter) == 0:
            lastpoint = 0
        else:
            lastpoint = Dokter[len(Dokter)-1].total_point

        totalpoint = (lastpoint + int(pointget)) - int(minuspoint)
        try:
            dokterPoint = TableLogPointDokter.objects.create(
                no_reg_dokter=kodereg,
                get_point=pointget,
                service=servicedid,
                total_point=totalpoint,
                minus_point=minuspoint,
            ).save()
            return JsonResponse({"message": "success"})
        except Exception:
            return HttpResponse(str(Exception))
