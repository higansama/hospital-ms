from user_management.models import TableDokter, TableAdmin, TableProvinsi, TableLogPointDokter, TablePerawat, TableFaskes, TablePoli, TableDivisi
from rest_framework import serializers
from goldenhour import helpers
from user_management.api.fasilitas import FaskesApi, PoliApi

# class DokterApi(serializers.ModelSerializer):
#    class Meta:
#         model = TableDokter
#         fields = ["id","username", "password", "first_name", "last_name", "id_faskes", "id_poli", "no_reg_dokter", "no_ktp"]
#         read_only_fields = ["no_reg_dokter"]
     
#    def create(self, validated_data):
#       countedID = TableDokter.objects.all()
#       validated_data["jenis_anggota"] = 2
#       validated_data["no_reg_dokter"] = helpers.RegistrationCodeGenerator(2, countedID.last(), countedID.count() ,validated_data["id_faskes"].faskes)
#       inst = TableDokter.objects.create(**validated_data)
#       return inst

class PerawatApi(serializers.ModelSerializer):
   class Meta:
        model = TablePerawat
        fields = "__all__"

class AdminApi(serializers.ModelSerializer):
   class Meta:
      model = TableAdmin
      fields = "__all__"

class ProvinsiApi(serializers.ModelSerializer):
   class Meta:
      model = TableProvinsi
      fields = "__all__"

   def create(self, validated_data):
      provinsi = TableProvinsi(
         provinsi=validated_data["provinsi"],
      ).save()
      return provinsi

class TableLogPointDokterApi(serializers.ModelSerializer):
   class Meta:
      model = TableLogPointDokter
      fields = "__all__"
