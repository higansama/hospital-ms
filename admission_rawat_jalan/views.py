from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from admission_rawat_jalan.api import *
from rest_framework.response import Response
# Create your views here.


class JadwalPraktekClass(viewsets.ModelViewSet):
    queryset = TableJadwalPraktekDokter.objects.all()
    serializer_class = TableJadwalPraktekDokterApi


class PraktekDokterClass(viewsets.ModelViewSet):
    queryset = TableKunjunganDokter.objects.all()
    serializer_class = TableKunjunganDokterApi

class TableAdmissionClass(APIView):
    def get(self, request, format=None):
        queryset = AdmissionRawatJalan.objects.all()
        serializer_class = TableAdmissionApi(queryset, many=True)
        return Response(serializer_class.data)

    def post(self, request, format=None):
        datarequest = TableAdmissionApi(data=request.data)
        if datarequest.is_valid():
            datarequest.save()
            return Response(datarequest.data,status=status.HTTP_201_CREATED)
        return Response(datarequest.errors, status=status.HTTP_400_BAD_REQUEST)

