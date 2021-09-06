from rest_framework import serializers
from user_management import models
from user_management.models import TableKelurahan, TableKota, TablePoli, TableProvinsi, TableKecamatan


class ProvinsiSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableProvinsi
        fields = ['id_provinsi', 'provinsi']

class KotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableKota
        fields = "__all__"


class KecamatanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableKecamatan
        fields = "__all__"
        

class KelurahanSerilizer(serializers.ModelSerializer):
    nama_kecamatan = serializers.CharField(source="id_kecamatan.kecamatan", read_only=True) 
    nama_kota = serializers.CharField(source="id_kecamatan.id_kota.kota", read_only=True) 
    nama_provinsi = serializers.CharField(source="id_kecamatan.id_kota.id_provinsi.provinsi", read_only=True)
    id_kota = serializers.CharField(source="id_kecamatan.id_kota.pk", read_only=True) 
    id_provinsi = serializers.CharField(source="id_kecamatan.id_kota.id_provinsi.pk", read_only=True)
    text = serializers.CharField(source="kelurahan", read_only=True)
    id = serializers.CharField(source="pk", read_only=True)

    class Meta:
        model = TableKelurahan
        fields = "__all__"
        


class PoliApi(serializers.ModelSerializer):
    faskes = serializers.CharField(source='id_faskes.faskes', read_only=True)
    alamatfaskes = serializers.CharField(source='id_faskes.alamat', read_only=True)
    kota_faskes = serializers.CharField(source='id_faskes.kota', read_only=True)

    class Meta:
        model = TablePoli
        fields = ["id" ,"poli", "id_faskes", "faskes", "kota_faskes", "alamatfaskes"]