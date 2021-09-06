import json
import re
from django.conf import settings
from django.http import Http404
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.utils.serializer_helpers import JSONBoundField
from rest_framework.views import APIView, status
from .api import *
from django.http import JsonResponse
from admission_rawat_jalan.api import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from user_management.models import TableUser
from rest_framework.permissions import IsAuthenticated
from admission_rawat_jalan.api import *
from goldenhour import helpers
import numpy
import datetime
from admission_rawat_jalan.models import TableJadwalPraktekDokter, AdmissionRawatJalan
from user_management.models import TableDokter
from dokter.api import *
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate
from django.core.paginator import Paginator
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q, base
# Create your views here.


class PasienDetail(APIView):
    def get_object(self, request):
        userID = helpers.JWTDecoder(request)['id']
        try:
            return TableUser.objects.get(pk=userID)
        except TableUser.DoesNotExist:
            raise Http404

    def get(self, request, tahun, bulan, tanggal, index, format=None):
        data = self.get_object(request)
        serializer = UserSerializer(data, many=False)
        return Response(serializer.data)


class PasienAdmission(PasienDetail):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        id = request.GET.get("id", "")
        JadwalAdmission = None
        if id == "":
            JadwalAdmission = AdmissionRawatJalan.objects.filter(
                no_reg_member=self.get_object(request)
            )
            serializer = TableAdmissionApi(JadwalAdmission, many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        else:
            JadwalAdmission = AdmissionRawatJalan.objects.get(pk=id)
            serializerJadwalAdmission = TableAdmissionApi(
                JadwalAdmission, many=False)
            AntrianQs = TableAntrian.objects.get(id_admission=JadwalAdmission)
            serializerAntrian = TableAntrianApi(AntrianQs, many=False)
            TableObatQs = TableObatPasien.objects.filter(
                id_admission_rawat_jalan=JadwalAdmission)
            TableObatSerial = TableObatApi(TableObatQs, many=True)
            return Response({"data_rawat_jalan": serializerJadwalAdmission.data, "antrian": serializerAntrian.data, "obat": TableObatSerial.data}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = TableAdmissionApi(data=request.data)
        pasien = self.get_object(request)
        if serializer.is_valid():
            createadmission = False
            antrianreturn = None
            try:
                objData = AdmissionRawatJalan.objects.all()
                idrawatjalan = helpers.AdmissionRawatJalanGenerator(
                    objData, serializer.validated_data["id_faskes"].faskes
                )
                serializer.validated_data["admission_rawat_jalan_id"] = idrawatjalan
                serializer.validated_data["no_reg_member"] = pasien
                serializer.validated_data["no_reg_dokter"] = serializer.validated_data["id_jadwal"].no_reg_dokter
                serializer.validated_data["status"] = 1
                serializer.validated_data["created_by"] = pasien.id
                serializer.validated_data["is_created_by_staff"] = False

                serializer.save()
                createadmission = True
            except Exception as e:
                return Response(Exception.__str__, status=status.HTTP_400_BAD_REQUEST)

            # create antrian
            if createadmission:
                # save no antrian
                noantrian = 1
                dataantrian = TableAntrian.objects.filter(
                    id_jadwal=serializer.data['id_jadwal'])
                if dataantrian.count() != 0:
                    noantrian = dataantrian.last().nomerantrian + 1
                antrian = TableAntrian()
                antrian.id_jadwal = TableJadwalPraktekDokter.objects.get(
                    pk=serializer.data['id_jadwal'])
                antrian.id_admission = AdmissionRawatJalan.objects.get(
                    pk=serializer.data['id'])
                antrian.nomerantrian = noantrian
                antrian.save()
                antrianreturn = TableAntrianApi(antrian)
            hasil = {
                "admissiondata": serializer.data,
                "antriandata": antrianreturn.data,
            }
            return Response(hasil)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasienAdmissionUpdate(PasienDetail):
    permission_classes = [IsAuthenticated]

    def put(self, request, idadmision, format=None):
        pasien = self.get_object(request)
        admission = AdmissionRawatJalan.objects.get(pk=idadmision)
        serializer = TableAdmissionApi(admission, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasienCheckin(APIView):
    permission_classes = [IsAuthenticated]
    # checkin pasien rawat jalan

    def put(self, request, idadmision, format=None):
        pasien = PasienDetail()
        pasien = pasien.get_object(request)
        objadm = AdmissionRawatJalan.objects.get(pk=idadmision)
        try:
            antrian = TableAntrian.objects.get(id_admission=objadm)
            antrian.status_checkin = True
            antrian.tanggal_checkin = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            antrian.valid = False
            antrian.save()
            return Response({"status": "success"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)


class PointPasien(PasienDetail):
    permission_classes = [IsAuthenticated]

    def get(self, request, jenis=None):
        pasien = self.get_object(request)
        queryset = TableLogPointUser.objects.filter(
            no_reg_member=pasien.no_reg_member)
        datajson = TableLogPointUserApi(queryset, many=True)
        if jenis == "last":
            queryset = TableLogPointUser.objects.filter(
                no_reg_member=pasien.no_reg_member).order_by('id').last()
            datajson = TableLogPointUserApi(queryset, many=False)
            return Response(datajson.data, status=status.HTTP_200_OK)
        datajson = TableLogPointUserApi(queryset, many=True)
        return Response(datajson.data, status=status.HTTP_200_OK)

    def post(self, request, jenis=None):
        serializer = TableLogPointUserApi(data=request.data)
        pasien = self.get_object(request)
        if serializer.is_valid():
            get_point = serializer.validated_data['get_point']
            minus_point = serializer.validated_data['minus_point']
            service = serializer.validated_data['service']
            lastpoint = TableLogPointUser.objects.filter(
                no_reg_member=pasien.no_reg_member).last()
            if lastpoint == None:
                lastpoint = 0
            else:
                lastpoint = lastpoint.total_point

            if jenis == "add":
                newpoint = lastpoint + int(get_point)
                pasienpoint = TableLogPointUser.objects.create(
                    no_reg_member=pasien.no_reg_member,
                    get_point=get_point,
                    service=service,
                    total_point=newpoint,
                    minus_point=0,
                ).save()
                return JsonResponse({"message": "Berhasil menambah point " + str(get_point)})
            elif jenis == "subtract":
                newpoint = lastpoint - int(minus_point)
                print(lastpoint)
                pasienpoint = TableLogPointUser.objects.create(
                    no_reg_member=pasien.no_reg_member,
                    get_point=0,
                    service=service,
                    total_point=newpoint,
                    minus_point=minus_point,
                ).save()
                return JsonResponse({"message": "Berhasil mengurangi point " + str(minus_point)})


class KeluargaClass(PasienDetail):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # user as a parent
        parentdata = self.get_object(request)
        qs = TableUserKeluarga.objects.filter(parent=parentdata.id)
        keluargajson = TableKeluargaApi(qs, many=True)
        return Response(keluargajson.data, status=status.HTTP_200_OK)

    def post(self, request):
        # user as a parent
        # no reg keluarga apakah dibuthkan?
        serializer = TableKeluargaApi(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['password'] = make_password("123456")
            serializer.validated_data['is_active'] = 1
            serializer.validated_data['jenis_anggota'] = 5
            serializer.validated_data['parent'] = self.get_object(request).id
            serializer.validated_data['no_reg_member'] = helpers.RegistrationPasienGenerator(
                5, TableUser.objects.all())
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": e.__str__()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            print("Error API")
            return Response({"error": serializer.errors})


class GetFaskes(APIView):
    def get(self, request, kota, format=None):
        qs = TableFaskes.objects.filter(status_faskes=1)
        namafaskes = request.GET.get("namafaskes", "")
        if kota != "all":
            qs = TableFaskes.objects.filter(kota__icontains=kota)

        serializer = FaskesSerializer(qs, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class DetailFaskes(APIView):
    def faskes_object(self, idfaskes):
        try:
            return TableFaskes.objects.get(pk=idfaskes)
        except:
            return Http404

    def get(self, request, idfaskes):
        qs = TableFaskes.objects.get(pk=idfaskes)
        serializer = FaskesSerializer(qs, many=False)
        return Response(serializer.data)


class PasienClass(APIView):
    def get(self, request, format=None):
        queryset = TableUser.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            countedID = TableUser.objects.all()
            noregis = helpers.RegistrationPasienGenerator(1, countedID)
            serializer.validated_data["jenis_anggota"] = 1
            serializer.validated_data["no_reg_member"] = noregis
            serializer.save()
            user = TableUser.objects.get(pk=serializer.data['id'])
            TableRekamMedis.objects.create(
                no_reg_member=user, no_reg_dokter=None).save()
            TableLogPointUser.objects.create(
                no_reg_member=noregis, get_point=500, total_point=500, service="Point Pendaftaran User Goldenhour").save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasienUpdateClass(PasienDetail):
    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        pasien = self.get_object(request)
        serializer = UserDetailSerializer(pasien, data=request.data)
        if serializer.is_valid():
            if pasien.jenis_anggota != 1:
                # ketika keluarga update data
                pasienkeluarga = TableUserKeluarga.objects.get(pk=pasien.id)
                pasienkeluarga.profile_updated = True
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        pasien = self.get_object(request)
        serializer = UserDetailSerializer(pasien, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

# @permission_classes((IsAuthenticated, ))


@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def UpdatePassword(request):
    # print(request.method == "")
    # return HttpResponse({"req": request.method == "POST"})
    if request.method == "POST":
        userClass = PasienDetail()
        user = userClass.get_object(request)
        new_password = request.POST.get('new_password')
        jsondata = UserAndPasswordApi(user, data=request.data)
        if jsondata.is_valid():
            username = user.username
            password = jsondata.validated_data["password"]
            auth = authenticate(username=username, password=password)
            if auth:
                # kalo dia child blok ini bakal running
                if user.jenis_anggota == 5:
                    objKeluarga = TableUserKeluarga.objects.get(pk=user.id)
                    objKeluarga.password_updated == True
                    objKeluarga.save()
                # kalo bukan child langsung aja save
                try:
                    jsondata.validated_data["password"] = make_password(
                        new_password)
                    jsondata.save()
                    return Response({"message": "Sukses"}, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"error": jsondata.errors()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PasienUploadPoto(PasienDetail):
    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        pasien = self.get_object(request)
        serializer = UserPoto(pasien, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RekamMedisClass(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request):
        tokendata = helpers.JWTDecoder(request)
        user = TableUser.objects.get(pk=tokendata['id'])
        print(user)
        try:
            return TableRekamMedis.objects.filter(no_reg_member=user)
        except TableUser.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        data = self.get_object(request)
        print(data)
        serializer = TableRekamMedisApi(data, many=True)
        return Response(serializer.data)

    def post(self, request, tahun, bulan, tanggal, index, format=None):
        data = self.get_object(request)
        inisial = self.get_object.nama
        # cek if initial tersebut sudah masuk ke table rekam medis atau belum start
        register = TableRekamMedis.objects.filter(
            no_rekam_medis__contains=inisial)
        status = False
        jumlah = 0
        if len(register) != 0:
            status = True

        # cek if initial tersebut sudah masuk ke table rekam medis atau belum stop
        no_rekam_medis = helpers.RekamMedisGenerator(
            status, register.count(), inisial)
        tindakan_pengobatan = request.POST.get("tindakan")
        diagnosa = request.POST.get("diagnosa", "")
        id_dokter = request.POST.get(
            "id_dokter", ""
        )  # harusnya ini bisa diganti dari id token
        rekamMedis = TableRekamMedis.objects.create(
            tindakan_pengobatan=tindakan_pengobatan,
            diagnosa=diagnosa,
            id_dokter=id_dokter,
            no_rekam_medis=no_rekam_medis,
            # tgl_pengobatan=tgl_pengobatan,
            # no_reg_member=no_reg_member,
        ).save()


@csrf_exempt
@api_view(["GET"])
def RekamMedisClassDetail(request, id):
    rm = TableRekamMedis.objects.get(pk=id)
    adm = AdmissionRawatJalan.objects.get(id=rm.id_admission)
    rmJson = TableRekamMedisApi(rm, many=False)
    admJson = TableAdmissionApi(adm, many=False)
    return Response({
        "rekammedis": rmJson.data,
        "admission": admJson.data,
    })


class GetDokterByIDPoli(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, idpoli, hari):
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

        if hari != "all":
            qs = TableJadwalPraktekDokter.objects.filter(
                id_poli=poli, jadwal_praktek=hari)
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
                        Q(id_jadwal=jadwal), Q(id_admission__tgl_kunjungan=tgl),~Q(id_admission__status=4) , Q(status_checkin=False)).count()
                    data = model_to_dict(jadwal)
                    data["namadokter"] = jadwal.no_reg_dokter.nama
                    data["jumlahpasien"] = getJmlhOrang
                    tmp["dokter"].append(json.dumps(data))
            result.append(tmp)
        return Response({"data": json.dumps(result)}, status=status.HTTP_200_OK)


class GetJadwalDokterByID(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, iddokter):
        dokter = TableDokter.objects.get(pk=iddokter)
        qs = TableJadwalPraktekDokter.objects.filter(no_reg_dokter=dokter)
        jsonjadwalbypoli = TableJadwalPraktekDokterApi(qs, many=True)
        return Response({"data": jsonjadwalbypoli.data}, status=status.HTTP_200_OK)

    def post(self, request, iddokter):
        # tanggal = request.POST.get()
        qs = TableJadwalPraktekDokter.objects.filter(no_reg_dokter=iddokter)
        jsonjadwalbypoli = TableJadwalPraktekDokterApi(qs, many=True)
        return Response({"data": jsonjadwalbypoli.data}, status=status.HTTP_200_OK)


@api_view(["POST"])
@csrf_exempt
def DetailJadwalDokter(request):
    if request.method == "POST":
        idjadwal = request.POST.get("idjadwal")
        print("idjadwal =>", idjadwal)
        titimangsa = request.POST.get("titimangsa")
        print("titimangsa =>", titimangsa)
        jadwal = TableJadwalPraktekDokter.objects.get(pk=idjadwal)
        getJmlhOrang = TableAntrian.objects.filter(
            Q(id_jadwal=jadwal), Q(id_admission__tgl_kunjungan=titimangsa)).count()
        data = model_to_dict(jadwal)
        data["namadokter"] = jadwal.no_reg_dokter.nama
        data["jumlahpasien"] = getJmlhOrang
        return Response({"data": json.dumps(data)}, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def UpdateUsernameDanEmail(request):
    pasien = request.user
    serializer = UsernameAndEmailApi(pasien, request.data)
    if serializer.is_valid():
        serializer.save()
        update_session_auth_hash(request, pasien)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def CancelRawatJalan(request, id):
    # set status 4 karena dibatalkan pasien
    admission = AdmissionRawatJalan.objects.get(pk=id)
    admission.status = 4
    admission.save()
    antrianBatal = TableAntrian.objects.get(id_admission=admission)
    antrianBatal.valid = 0
    antrianBatal.nomerantrian = 0
    antrianBatal.status_checkin = False
    antrianBatal.save()
    titimangsa = admission.tgl_kunjungan
    idjadwal = admission.id_jadwal
    listorangantri = TableAntrian.objects.filter(~Q(nomerantrian=0), Q(
        id_admission__tgl_kunjungan=titimangsa), Q(id_jadwal=idjadwal))
    noantri = 1
    for data in listorangantri:
        print(data.nomerantrian)
        data.nomerantrian = noantri
        noantri += 1
    TableAntrian.objects.bulk_update(listorangantri, ['nomerantrian'])
    return Response(json.dumps({"msg": "success"}), status=status.HTTP_200_OK)

