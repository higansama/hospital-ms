import json
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
import numpy
from rest_framework.decorators import api_view, permission_classes
from user_management.api.fasilitas import *
from django.http import HttpResponse, JsonResponse, Http404, response
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from admission_rawat_jalan.models import AdmissionRawatJalan
from admission_rawat_jalan.api import TableAdmissionApi
from rest_framework.permissions import IsAuthenticated
from user_management.models import TableAdmin
from frontdesk.api import *
from dokter.api import TableJadwalDokterApi, DokterApi, TableKunjunganApi
from .jwtclaim import AdminTokenSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from admission_rawat_jalan.api import *
# Create your views here.


class FrontDeskClass(viewsets.ModelViewSet):
    # CRUD
    queryset = TableAdmin.objects.all()
    serializer_class = AdminApi


class FaskesAdmin(viewsets.ModelViewSet):
    queryset = TableFaskes.objects.all()
    serializer_class = FaskesApi
    permission_classes = [IsAuthenticated]


class FrontDeskDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request):
        user = helpers.JWTDecoder(request)
        try:
            return TableAdmin.objects.get(pk=user['user_id'])
        except Exception as e:
            return Http404

    def get(self, request):
        user = self.get_object(request)
        jsonUser = AdminApi(user, many=False)
        return Response(jsonUser.data, status=status.HTTP_200_OK)

    def put(self, request):
        admin = self.get_object(request)
        serializer = AdminApi(admin, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FrontdeskRawatJalan(FrontDeskDetail):
    def get(self, request, idstaff, idfaskes):
        queryset = AdmissionRawatJalan.objects.filter(id_faskes=idfaskes)
        serializer_class = TableAdmissionApi(queryset, many=True)
        return Response(serializer_class.data)

    def post(self, request, idstaff, idfaskes):
        datarequest = TableAdmissionApi(data=request.data)
        if datarequest.is_valid():
            datarequest.save()
            return Response(datarequest.data, status=status.HTTP_201_CREATED)
        return Response(datarequest.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckinRawatJalan(FrontDeskDetail):
    def put(self, request, idstaff, idfaskes, idrawatjalan, statusparam):
        #         time validation is not installed
        statuscheckin = False
        if statusparam == "1":
            statuscheckin = True
        objadm = AdmissionRawatJalan.objects.get(pk=idrawatjalan)
        try:
            antrian = TableAntrian.objects.get(id_admission=objadm)
            antrian.status_checkin = statuscheckin
            antrian.tanggal_checkin = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            antrian.valid = False
            antrian.save()
            return Response({"status": "success"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)


class FrontdeskRawatJalanDetail(APIView):
    def get_object(self, pk):
        try:
            return AdmissionRawatJalan.objects.get(pk=pk)
        except AdmissionRawatJalan.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        query = self.get_object(pk)
        print("Query =>", query)
        serializer = TableAdmissionApi(query, many=False)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        admission = self.get_object(pk)
        serializer = TableAdmissionApi(admission, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DokterJadwal(APIView):
    def get_dokter(iddokter):
        try:
            return TableDokter.objects.get(pk=iddokter)
        except Exception as e:
            return Http404

    def get(self, request, iddokter):
        qs = TableJadwalPraktekDokter.objects.filter(no_reg_dokter=iddokter)
        jadwaljson = TableJadwalDokterApi(qs, many=True)
        return Response(jadwaljson.data)

    def post(self, request, iddokter):
        serializer = TableJadwalDokterApi(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["no_reg_dokter"] = TableDokter.objects.get(
                pk=iddokter)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginProcess(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = AdminTokenSerializer


@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def AddRawatJalanOtomatis(request):
    id_jadwal = request.POST.get("id_jadwal")
    nomerantrian = request.POST.get("nomerantrian")
    titimangsa = request.POST.get("titimangsa")
    no_ktp = request.POST.get("no_ktp")
    nama = request.POST.get("nama")
    no_ponsel = request.POST.get("no_ponsel")
    jenis_kelamin = request.POST.get("jenis_kelamin")
    email = request.POST.get("email")
    gejala = request.POST.get("gejala")
    # createusername
    result = {}
    try:
        user = TableUser()
        user.username = helpers.usernameGenerator(nama, no_ponsel)
        user.nama = nama
        user.no_ponsel = no_ponsel
        user.email = email
        user.no_ktp = no_ktp
        user.jenis_kelamin = True if jenis_kelamin == True else False
        user.is_active = 1
        user.no_reg_member = helpers.RegistrationPasienGenerator(
            2, TableUser.objects.all())
        user.save()
        result["user"] = user
    except Exception as e:
        return Response({"error buat user": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # daftar rawat jalan
        jadwal = TableJadwalPraktekDokter.objects.get(pk=id_jadwal)
        admission = AdmissionRawatJalan()
        admission.no_reg_member = user
        admission.admission_rawat_jalan_id = helpers.AdmissionRawatJalanGenerator(
            AdmissionRawatJalan.objects.all(), jadwal.id_faskes.faskes)
        admission.id_poli = jadwal.id_poli
        admission.id_faskes = jadwal.id_faskes
        admission.id_jadwal = jadwal
        admission.no_reg_dokter = jadwal.no_reg_dokter
        admission.tgl_kunjungan = titimangsa
        admission.jam_kunjungan = jadwal.jam_mulai
        admission.gejala = gejala
        admission.created_by = request.user.id
        admission.is_created_by_staff = True
        admission.save()
        result["admission"] = admission
    except Exception as e:
        return Response({"error buat admission": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # buat antrian
        antrian = TableAntrian()
        antrian.id_jadwal = jadwal
        antrian.id_admission = admission
        antrian.status_checkin = True
        getAntrian = TableAntrian.objects.filter(
            id_jadwal=jadwal, id_admission__tgl_kunjungan=titimangsa).count() + 1
        antrian.nomerantrian = getAntrian
        antrian.save()
        print(antrian)
        result["antrian"] = antrian
    except Exception as e:
        return Response({"error buat antrian": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"data": "berhasil"}, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def GetDokterByFaskesDanPoli(request, idfaskes, idpoli):
    faskes = TableFaskes.objects.get(pk=idfaskes)
    poli = TablePoli.objects.get(pk=idpoli)
    dokters = TableDokter.objects.filter(id_poli=poli, id_faskes=faskes)
    dokterJson = DokterApi(dokters, many=True)
    return Response({"data": dokterJson.data}, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def AntrianByID(request, idjadwal, titimangsa):
    jadwal = TableJadwalPraktekDokter.objects.get(pk=idjadwal)
    antrian = TableAntrian.objects.filter(
        id_jadwal=jadwal, id_admission__tgl_kunjungan=titimangsa)
    antrianJson = TableAntrianApi(antrian, many=True)
    return Response(antrianJson.data, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def CheckinPasien(request, idantrian):
    antrian = TableAntrian.objects.get(pk=idantrian)
    antrian.status_checkin = True
    antrian.save()
    return Response(json.dumps({"msg": "Berhasil"}), status=status.HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def checkinDokter(request, idjadwal):
    try:
        jadwal = TableJadwalPraktekDokter.objects.get(pk=idjadwal)
        kunjungan = TableKunjunganDokter()
        kunjungan.no_reg_dokter = jadwal.no_reg_dokter
        kunjungan.id_jadwal = jadwal
        kunjungan.status_jadwal = 1
        kunjungan.save()
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=status.HTTP_400_BAD_REQUEST)
    return Response(json.dumps({"message": "success"}), status=status.HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getJadwalPraktekDokter(request, idpoli):
    baseTgl = request.GET.get("base", "")
    today = datetime.date.today()
    basedate = None
    if int(baseTgl) < 0:
        basedate = today - datetime.timedelta(days=(int(baseTgl) * -1))
    elif int(baseTgl) > 0:
        basedate = today + datetime.timedelta(days=int(baseTgl))
    elif int(baseTgl) == 0:
        basedate = datetime.datetime.now()
    if idpoli != "all":
        poli = TablePoli.objects.get(pk=idpoli)
        qs = TableJadwalPraktekDokter.objects.filter(id_poli=poli)
    else:
        qs = TableJadwalPraktekDokter.objects.all()
    arrDate = numpy.array(
        [basedate + datetime.timedelta(days=i) for i in range(7)])
    result = []
    for dataTgl in arrDate:
        tgl = dataTgl.strftime("%Y-%m-%d")
        tmp = {
            dataTgl.weekday(): dataTgl.day,
            "tanggal": str(dataTgl),
            "dokter": [],
        }
        for jadwal in qs:
            if str(jadwal.jadwal_praktek) == str(dataTgl.weekday()):
                getJmlhOrang = TableAntrian.objects.filter(
                    Q(id_jadwal=jadwal), Q(id_admission__tgl_kunjungan=tgl)).count()
                data = model_to_dict(jadwal)
                data["namadokter"] = jadwal.no_reg_dokter.nama
                data["jumlahpasien"] = getJmlhOrang
                data["namapoli"] = jadwal.id_poli.poli
                tmp["dokter"].append(json.dumps(data))
        result.append(tmp)
    return Response({"data": json.dumps(result)}, status=status.HTTP_200_OK)

    # hari = 0
    # result = []
    # for hari in range(7):
    #     dokterList = TableJadwalPraktekDokter.objects.filter(no_reg_dokter__id_faskes= faskes, jadwal_praktek=hari)
    #     result.append(dokterList)
    #     hari += 1
