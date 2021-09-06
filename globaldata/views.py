from user_management.api.fasilitas import FaskesApi
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from user_management.models import *
from django.http import HttpResponse, JsonResponse, request
from django.views.decorators.csrf import csrf_exempt
from goldenhour import helpers
from django.forms.models import model_to_dict
from globaldata.api import *
from django.http import QueryDict
from pasien.views import DetailFaskes
# Create your views here.
@csrf_exempt
def Provinsi(request, id=None):
    provinsi = TableProvinsi
    if request.method == "GET":
        q = request.GET.get("q","")
        if q:
            listdata = provinsi.objects.filter(provinsi__contains=q)
            data = ProvinsiSerializer(listdata)
            return HttpResponse(data.data, content_type='application/json')
        else:
            listprovinsi = TableProvinsi.objects.all()
            data = ProvinsiSerializer(listprovinsi, many=True)
            return JsonResponse(data.data, safe=False)

    if request.method == "POST":
        nama_provinsi = request.POST.get("provinsi", "")
        try:
            TableProvinsi.objects.create(provinsi=nama_provinsi).save()
        except Exception as e:
            return HttpResponse(e)
        return HttpResponse("Sukses")
    
    if request.method == "DELETE":
        try:
            provinsi.objects.get(pk=id).delete()
            return HttpResponse("Sukses")
        except Exception as e:
            return HttpResponse(e)
    if request.method == "PUT":
        val = QueryDict(request.body)
        print(val)
        return HttpResponse(request.PUT["provinsi"])
        # try:
        #     prov = provinsi.objects.get(pk=id)
        # except Exception as e:
            # return HttpResponse(e)

class GetPoliByFaskes(DetailFaskes):
    def get(self, request, idfaskes):
        try:
            faskes = self.faskes_object(idfaskes)
            qs = TablePoli.objects.all()
            if idfaskes != "all":
                qs = TablePoli.objects.filter(id_faskes=faskes)
            polijson = PoliApi(qs, many=True)
            return Response({"data": polijson.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, idfaskes):
        poli = PoliApi(data=request.data)
        if poli.is_valid():
            poli.save()
            return Response(poli.data, status=status.HTTP_200_OK)
        return Response(poli.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProvinsiClass(viewsets.ModelViewSet):
    queryset = TableProvinsi.objects.all()
    serializer_class = ProvinsiSerializer



@api_view(['GET', 'POST'])
def KotaController(request):
    if request.method == "GET":
        idprovinsi = request.GET.get('idprovinsi')
        qs = TableKota.objects.filter(id_provinsi=idprovinsi)
        jsonKota = KotaSerializer(qs, many=True)
        return Response(jsonKota.data, status=status.HTTP_200_OK)
    
    if request.method == "POST":
        jsonKota = KotaSerializer(data=request.data)
        if jsonKota.is_valid():
            jsonKota.save()
            return Response(jsonKota.data, status=status.HTTP_200_OK)
        return Response(jsonKota.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@api_view(['GET', 'POST'])
def KecamatanKontroller(request):
    if request.method == "GET":
        idkota = request.GET.get('idkota')
        qs = TableKecamatan.objects.filter(id_kota=idkota)
        jsonkecamatan = KecamatanSerializer(qs, many=True)
        return Response(jsonkecamatan.data, status=status.HTTP_200_OK)
    
    if request.method == "POST":
        jsonKota = KecamatanSerializer(data=request.data)
        if jsonKota.is_valid():
            jsonKota.save()
            return Response(jsonKota.data, status=status.HTTP_200_OK)
        return Response(jsonKota.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


@api_view(['GET', 'POST'])
def KelurahanKontoler(request):
    if request.method == "GET":
        idkecamatan = request.GET.get('idkecamatan')
        qs = TableKelurahan.objects.filter(id_kecamatan=idkecamatan)
        jsonkecamatan = KelurahanSerilizer(qs, many=True)
        return Response(jsonkecamatan.data, status=status.HTTP_200_OK)
    
    if request.method == "POST":
        jsonKelurahan = KelurahanSerilizer(data=request.data)
        if jsonKelurahan.is_valid():
            jsonKelurahan.save()
            return Response(jsonKelurahan.data, status=status.HTTP_200_OK)
        return Response(jsonKelurahan.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST'])
def CariKelurahan(request):
    if request.method == "GET":
        namakelurahan = request.GET.get("q", "")
        qs = None
        if namakelurahan == "":
            qs = TableKelurahan.objects.all()
        else:
            qs = TableKelurahan.objects.filter(kelurahan__icontains=namakelurahan)
        qsJson = KelurahanSerilizer(qs, many=True)
        return Response(qsJson.data, status=status.HTTP_200_OK)
        
@api_view(['GET'])
@csrf_exempt
def FaskesDetail(request, idfaskes):
    try:
        faskesdetail = TableFaskes.objects.get(pk=idfaskes)
        listpoli = TablePoli.objects.filter(id_faskes=faskesdetail)
        jsonFaskesDetail = FaskesApi(faskesdetail, many=False)
        jsonPoli = PoliApi(listpoli, many=True)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"faskes": jsonFaskesDetail.data, "poli": jsonPoli.data }, status=status.HTTP_200_OK)

