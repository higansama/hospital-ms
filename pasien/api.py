from django.db.models.fields import CharField
from user_management.models import *
from rest_framework import serializers
from goldenhour import helpers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableUser
        fields = "__all__"


class TableRekamMedisApi(serializers.ModelSerializer):
    class Meta:
        model = TableRekamMedis
        fields = "__all__"


class TableLogPointUserApi(serializers.ModelSerializer):
    class Meta:
        model = TableLogPointUser
        fields = "__all__"


class TableKeluargaApi(serializers.ModelSerializer):
    class Meta:
        model = TableUserKeluarga
        fields = ["nama", "username", "last_login", "email", "no_telepon",
                  "no_ponsel", "no_reg_member", "foto_identitas", "hubungan_keluarga"]
        read_only_fields = ["password", "parent", "last_login"]


class FaskesSerializer(serializers.ModelSerializer):
    provinsi = serializers.CharField(
        source="kelurahan.id_kecamatan.id_kota.id_provinsi.provinsi", read_only=True)
    kota = serializers.CharField(
        source="kelurahan.id_kecamatan.id_kota.kota", read_only=True)
    kecamatan = serializers.CharField(
        source="kelurahan.id_kecamatan.kecamatan", read_only=True)
    kelurahan = serializers.CharField(
        source="kelurahan.kelurahan", read_only=True)

    class Meta:
        serializers.CharField(source="provinsi_utama.provinsi", read_only=True)
        model = TableFaskes
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableUser
        fields = ["id", "username", "password",
                  "email", "no_ktp", "no_reg_member"]

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.is_active = 1
        user.save()
        return user


class UserDetailSerializer(serializers.ModelSerializer):
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
        model = TableUser
        fields = "__all__"
        read_only_fields = ["password", "jenis_anggota"]


class UserAndPasswordApi(serializers.ModelSerializer):
    class Meta:
        model = TableUser
        fields = ["password"]


class UsernameAndEmailApi(serializers.ModelSerializer):
    class Meta:
        model = TableUser
        fields = ["username", "email"]


class UserPoto(serializers.ModelSerializer):
    class Meta:
        model = TableUser
        fields = ["foto_identitas"]

# class DetailRekamMedis(serializers.Serializer):
