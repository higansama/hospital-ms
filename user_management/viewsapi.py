from user_management.models import *
from user_management.api.dokter_api import *
from user_management.api.user_api import *
from user_management.api.fasilitas import *
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

def Faskes(request):
    pass
    # if request.method == "POST":
    #     nama = request.POST.get("faskes", "")
    #     alamat = request.POST.get("alamat", "")
    #     try:
    #         TableFaskes.objects.create(
    #             faskes=nama,
    #             alamat=alamat,
    #         ).save()
    #         return JsonResponse({"message": "sukses", "no_reg_perawat": no_reg_perawat})
    #     except Exception as e:
    #         return HttpResponse(str(e))
    # if request.method == "GET":
    #     qs = TableFaskes.objects.all()
    #     sqs = FaskesApi(qs, many=True)
    #     return JsonResponse(
    #         {
    #             "code": 200,
    #             "message": "success",
    #             "data": sqs.data,
    #         }
    #     )


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
            serializer.validated_data["jenis_anggota"] = 2
            serializer.validated_data["no_reg_member"] = noregis
            serializer.validated_data["is_active"] = 1
            serializer.save()
            user= TableUser.objects.get(pk=serializer.data['id'])
            TableRekamMedis.objects.create(no_reg_member=user, no_reg_dokter=None).save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasienUpdateClass(APIView):
    def put(self, request,idpasien , format=None):
        pasien = TableUser.objects.get(pk=idpasien)
        serializer = UserSerializer(pasien, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasienDetail(APIView):
    # /account/user/rekammedis/2021/04/13/1
    def get_object(self, tahun, bulan, tanggal, index):
        noreg = tahun + "/" + bulan + "/" + tanggal + "/" + index
        try:
            return TableUser.objects.get(noreg=noreg)
        except TableUser.DoesNotExist:
            raise Http404

    def get(self, request, tahun, bulan, tanggal, index, format=None):
        return self.get_object(tahun, bulan, tanggal, index)


# class RekamMedisClass(APIView):
#     permission_classes = [IsAuthenticated]
#     def get_object(self, tahun, bulan, tanggal, index):
#         noreg = tahun + "/" + bulan + "/" + tanggal + "/" + index
#         try:
#             return TableRekamMedis.objects.get(no_reg_member=noreg)
#         except TableUser.DoesNotExist:
#             raise Http404

#     def get(self, request, tahun, bulan, tanggal, index, format=None):
#         print(request.get_header())
#         data = self.get_object(tahun, bulan, tanggal, index)
#         serializer = TableRekamMedisApi(data, many=True)
#         return Response(serializer.data)

#     def post(self, request, tahun, bulan, tanggal, index, format=None):
#         data = self.get_object(tahun, bulan, tanggal, index)
#         inisial = self.get_object.nama
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
#         rekamMedis = TableRekamMedis.objects.create(
#             tindakan_pengobatan=tindakan_pengobatan,
#             diagnosa=diagnosa,
#             id_dokter=id_dokter,
#             no_rekam_medis=no_rekam_medis,
#             # tgl_pengobatan=tgl_pengobatan,
#             no_reg_member=no_reg_member,
#         ).save()


class PoliClass(viewsets.ModelViewSet):
    queryset = TablePoli.objects.all()
    serializer_class = PoliApi


class FaskesClass(viewsets.ModelViewSet):
    queryset = TableFaskes.objects.all()
    serializer_class = FaskesApi


class DivisiClass(viewsets.ModelViewSet):
    queryset = TableDivisi.objects.all()
    serializer_class = DivisiApi


# def get(self, request, format=None):
#     queryset = TableDivisi.objects.all()
#     serializer = DivisiApi(queryset, many=True)
#     return Response(serializer.data)

# def post(self, request, format=None):
#     serializer = DivisiApi(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
