from user_management.models import *
from admission_rawat_jalan.models import *
from rest_framework import serializers
from goldenhour import helpers
from user_management.api.fasilitas import FaskesApi, PoliApi
from django.contrib.auth.hashers import make_password

class FaskesApi(serializers.ModelSerializer):
   class Meta:
      model = TableFaskes
      fields = "__all__"

class DokterApi(serializers.ModelSerializer):
   faskes = serializers.CharField(source='id_faskes.faskes', read_only=True)
   class Meta:
        model = TableDokter
      #   fields = "__all__"
        fields = ["id","username", "password", "first_name", "nama", "last_name", "id_poli", "no_reg_dokter", "no_ktp", "faskes", "id_faskes"]
        read_only_fields = ["no_reg_dokter", "faskes"]

   def create(self, validated_data):
      countedID = TableDokter.objects.all()
      validated_data["jenis_anggota"] = 2
      validated_data["is_active"] = 1
      validated_data["password"] = make_password(validated_data['password'])
      validated_data["no_reg_dokter"] = helpers.RegistrationCodeGenerator(2, countedID.last(), countedID.count() ,validated_data["id_faskes"].faskes)
      inst = TableDokter.objects.create(**validated_data)
      return inst


class LogPointDokter(serializers.ModelSerializer):
   class Meta:
      model = TableLogPointDokter
      fields = "__all__"
   
class TableRekamMedisApi(serializers.ModelSerializer):
   class Meta:
      model = TableRekamMedis
      fields = "__all__"

class TablePointDokterApi(serializers.ModelSerializer):
   class Meta:
      model = TableLogPointDokter
      fields = "__all__"


class TableJadwalDokterApi(serializers.ModelSerializer):
   # no_reg_dokter = serializers.CharField(source='no_reg_dokter.no_reg_dokter', read_only=True)
   nama = serializers.CharField(source='no_reg_dokter.nama',read_only=True)
   faskes = serializers.CharField(source='id_faskes.faskes',read_only=True)
   poli = serializers.CharField(source='id_poli.poli',read_only=True)
   alamat_faskes = serializers.CharField(source='id_faskes.alamat',read_only=True)
   class Meta:
      model = TableJadwalPraktekDokter
      fields = ["id","id_poli","poli","id_faskes","faskes", "alamat_faskes","jadwal_praktek","jam_mulai","jam_selesai", "nama"]
      read_only = ["no_reg_dokter"]

class TableKunjunganApi(serializers.ModelSerializer):
   # no_reg_dokter = serializers.CharField(source='no_reg_dokter.no_reg_dokter',read_only=True)
   nama = serializers.CharField(source='no_reg_dokter.nama',read_only=True)
   faskes = serializers.CharField(source='no_reg_dokter.id_faskes.faskes',read_only=True)
   poli = serializers.CharField(source='no_reg_dokter.id_poli.poli',read_only=True)
   class Meta:
      model = TableKunjunganDokter
      fields = ["id","nama","no_reg_dokter","id_poli", "poli","id_faskes", "faskes","id_jadwal","jumlah_pasien","status_jadwal"]

   