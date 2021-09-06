from builtins import print

from rest_framework.fields import ReadOnlyField
from user_management.models import *
from admission_rawat_jalan.models import *
from rest_framework import serializers
from goldenhour import helpers
from django.contrib.auth.hashers import make_password


class AdminApi(serializers.ModelSerializer):
    faskes = serializers.CharField(source='id_faskes.faskes', read_only=True)
    divisi = serializers.CharField(source='divisi_id.divisi', read_only=True)
    nama_provinsi_utama = serializers.CharField(
        source="provinsi_utama.provinsi", read_only=True)
    nama_kota_utama = serializers.CharField(
        source="kota_utama.kota", read_only=True)
    nama_kecamatan_utama = serializers.CharField(
        source="kecamatan_utama.kecamatan", read_only=True)
    nama_kelurahan_utama = serializers.CharField(
        source="kelurahan_utama.kelurahan", read_only=True)
    nama_provinsi_domisili = serializers.CharField(
        source="provinsi_domisili.provinsi", read_only=True)
    nama_kota_domisili = serializers.CharField(
        source="kota_domisili.kota", read_only=True)
    nama_kecamatan_domisili = serializers.CharField(
        source="kecamatan_domisili.kecamatan", read_only=True)
    nama_kelurahan_domisili = serializers.CharField(
        source="kelurahan_domisili.kelurahan", read_only=True)

    class Meta:
        model = TableAdmin
        read_only_field = ["no_reg_admin"]
        fields = ["id", "username", "password", "nama", "gh_admin", "divisi_id", "divisi", "faskes", "id_faskes", "no_telepon", "no_ponsel", "tingkat_pendidikan", "kodepos_utama", "kodepos_domisili", "alamat_utama", "alamat_domisili", "kelurahan_utama",
                  "kecamatan_utama", "kota_utama", "provinsi_utama", "kelurahan_domisili", "kecamatan_domisili", "kota_domisili", "provinsi_domisili", "tempat_lahir", "tgl_lahir", "jenis_kelamin", "no_asuransi", "status_keanggotaan", "foto_identitas", "nama_provinsi_utama", "nama_kota_utama", "nama_kecamatan_utama", "nama_kelurahan_utama", "nama_provinsi_domisili", "nama_kota_domisili", "nama_kecamatan_domisili", "nama_kelurahan_domisili"]

    def create(self, validated_data):
        countedID = TableAdmin.objects.all()
        validated_data["jenis_anggota"] = 4
        validated_data["is_active"] = 1
        validated_data["password"] = make_password(validated_data["password"])
        if validated_data["id_faskes"] != None:
            validated_data["no_reg_admin"] = helpers.RegistrationStaff(
                countedID.count(), validated_data["id_faskes"].faskes)
        else:
            validated_data["no_reg_admin"] = helpers.RegistrationStaff(
                countedID.count(), "Golden Hour")
        # if validated_data["gh_admin"] == "1":
        #     validated_data["divisi_id"] = None
        #     validated_data["id_faskes"] = None
        inst = TableAdmin.objects.create(**validated_data)
        return inst
