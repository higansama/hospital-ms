from rest_framework import viewsets, status
from rest_framework.views import APIView, Response
from dokter.api import *
from user_management.models import TableUser, TableRekamMedis
from django.http import Http404, HttpResponse
from admission_rawat_jalan.models import *
from admission_rawat_jalan.api import *
# from user_management.api.user_api import TableRekamMedisApi
from .auth import DokterTokenSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
import datetime
from django.db.models import Q
class DokterTokenSerializer(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = DokterTokenSerializer


class DokterClass(viewsets.ModelViewSet):
    queryset = TableDokter.objects.all()
    serializer_class = DokterApi

class DetailDokter(APIView):
    def get_object(self, request):
        user = helpers.JWTDecoder(request)
        try:
            return TableDokter.objects.get(pk=user['user_id'])
        except Exception as e:
            return Http404
    
    def get_member(self, iduser):
        try:
            return TableUser.objects.get(pk=iduser)        
        except Exception:
            return Http404()
        

    def get(self, request):
        context_serializer = {'request': request}
        dokter = self.get_object(request)
        dokterjson = DokterApi(dokter, many=False)
        return Response(dokterjson.data)


    def put(self, request):
        dokter = self.get_object(request)
        dokterjson = DokterApi(dokter, data=request.data)
        if dokterjson.is_valid():
            dokterjson.save()
            return Response(dokterjson.data)
        return Response(dokterjson.errors, status=status.HTTP_400_BAD_REQUEST)

class DokterPoints(DetailDokter):
    permission_classes = [IsAuthenticated]
    def get(self, request, jenis=None):
        dokter = self.get_object(request)
        pointdokter = TableLogPointDokter.objects.filter(no_reg_dokter=dokter.no_reg_dokter)
        pointjson = TablePointDokterApi(pointdokter, many=True)
        return Response(pointjson.data, status=status.HTTP_200_OK)
    
    def post(self, request, jenis=None):
        dokter = self.get_object(request)
        serializer = LogPointDokter(data=request.data)
        if serializer.is_valid():
            get_point = serializer.data['get_point']
            minus_point = serializer.data['minus_point']
            service = serializer.data['service']
            lastpoint = TableLogPointDokter.objects.filter(no_reg_dokter=dokter.no_reg_dokter).last()
            if lastpoint == None:
                lastpoint = 0
            else:
                lastpoint = lastpoint.total_point
            if jenis == "add":
                    newpoint = int(lastpoint) + int(get_point)
                    dokterPoint = TableLogPointDokter.objects.create(
                    no_reg_dokter=dokter.no_reg_dokter,
                    get_point=get_point,
                    service=service,
                    total_point=newpoint,
                    minus_point=0,
                    ).save()
                    return Response(dokterPoint)
            elif jenis == "subtract":
                    newpoint = int(lastpoint) - int(get_point)
                    dokterPoint = TableLogPointDokter.objects.create(
                    no_reg_dokter=dokter.no_reg_dokter,
                    get_point=get_point,
                    service=service,
                    total_point=newpoint,
                    minus_point=0,
                    ).save()
                    return Response(dokterPoint)

class DokterJadwal(DetailDokter):
    permission_classes = [IsAuthenticated]

    def get(self, request, id=""):
        dokter = self.get_object(request)
        qs = TableJadwalPraktekDokter.objects.filter(no_reg_dokter=dokter)
        jadwaljson = TableJadwalDokterApi(qs, many=True)
        return Response(jadwaljson.data)

    def post(self, request, id=""):
        dokter = self.get_object(request)
        serializer = TableJadwalDokterApi(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["no_reg_dokter"] = dokter
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, id):
        dokter = self.get_object(request)
        jadwal = TableJadwalPraktekDokter.objects.get(pk=id)
        serializer = TableJadwalDokterApi(jadwal, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DokterKunjungan(DetailDokter):
    permission_classes = [IsAuthenticated]
    def get(self, request, nama_faskes, tahun, bulan, tgl, no_urut):
        dokter = self.get_object(request)
        queryset = TableKunjunganDokter.objects.filter(no_reg_dokter=dokter)
        kunjunganjson = TableKunjunganApi(queryset, many=True)
        return Response(kunjunganjson.data)
    
    def post(self, request, nama_faskes, tahun, bulan, tgl, no_urut):
        dokter = self.get_object(request)
        serializer = TableKunjunganApi(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DokterKonfirmasiKunjungan(DetailDokter):
    permission_classes = [IsAuthenticated]
    def put(self,  request, idkunjungan, statuskunjungan):
        try:
            kunjungan = TableKunjunganDokter.objects.get(pk=idkunjungan)
            kunjungan.status_jadwal = statuskunjungan
            kunjungan.save()
            return Response(TableKunjunganApi(kunjungan).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class DokerDiagnosa(DetailDokter):
    permission_classes = [IsAuthenticated]
    def get(self,  request, iduser):
        qs = TableRekamMedis.objects.filter(no_reg_member=self.get_member(iduser))
        rekammedisjson = TableRekamMedisApi(qs, many=True)
        return Response(rekammedisjson.data, status=status.HTTP_200_OK)


    def post(self,  request, iduser):
        serializer = TableRekamMedisApi(data=request.data)
        if serializer.is_valid():
            pasien = TableUser.objects.get(pk=iduser)
            rm = TableRekamMedis.objects.filter(no_reg_member=pasien)
            serializer.validated_data["no_reg_dokter"] = self.get_object(request)
            serializer.validated_data["no_reg_member"] = pasien
            serializer.validated_data["tgl_pengobatan"] = helpers.TAHUN + "-" + helpers.BULAN + "-" + helpers.TANGGAL
            serializer.validated_data["no_rekam_medis"] = helpers.RekamMedisGenerator(pasien, rm)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
# @permission_classes((IsAuthenticated))
def KunjunganDokter(request, idkunjungan):
    jadwal = TableJadwalPraktekDokter.objects.get(pk=idkunjungan)
    tanggal = helpers.TANGGAL + "-" + helpers.BULAN + "-" + helpers.TAHUN
    hari = datetime.datetime.today().weekday()
    qs = TableAntrian.objects.filter(Q(id_jadwal=jadwal))
    jsonqs = TableAntrianApi(qs, many=True)
    return Response(jsonqs.data, status=status.HTTP_200_OK)