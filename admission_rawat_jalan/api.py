from django.db.models.fields import CharField
from rest_framework import serializers
from admission_rawat_jalan.models import (
    TableKunjunganDokter,
    TableJadwalPraktekDokter,
    AdmissionRawatJalan,
    TableAntrian,
    TableObatPasien,
)
from goldenhour import helpers
from django.db.models import Q
from django.db import connection

class TableKunjunganDokterApi(serializers.ModelSerializer):
    class Meta:
        model = TableKunjunganDokter
        fields = "__all__"


class TableJadwalPraktekDokterApi(serializers.ModelSerializer):
    namadokter = serializers.CharField(source='no_reg_dokter.nama', read_only=True)
    id_dokter = serializers.CharField(source='no_reg_dokter.id', read_only=True)
    
    class Meta:
        model = TableJadwalPraktekDokter
        fields = "__all__"


class TableAdmissionApi(serializers.ModelSerializer):
    faskes = serializers.CharField(source='id_faskes.faskes', read_only=True)
    alamat_faskes = serializers.CharField(source='id_faskes.alamat', read_only=True)
    poli = serializers.CharField(source='id_poli.poli', read_only=True)
    namadokter = serializers.CharField(source='no_reg_dokter.nama', read_only=True)
    class Meta:
        model = AdmissionRawatJalan
        fields = "__all__"
        read_only_fields = ["admission_rawat_jalan_id", "no_reg_member", "no_reg_dokter"]


    def create(self, validated_data):
        admission = super(TableAdmissionApi, self).create(validated_data)
        return admission

        # noantri = TableAntrian.objects.create(
        #     id_admission=inst,
        #     status_checkin=False,
        #     nomerantrian=noantrian,
        #     id_jadwal=validate_data["id_jadwal"],
        # ).save()
        # #
        # return inst

    def update(self, instance, validated_data):
        instance.id = validated_data.get("id", instance.id)
        instance.admission_rawat_jalan_id = validated_data.get(
            "admission_rawat_jalan_id", instance.admission_rawat_jalan_id
        )
        instance.no_reg_member = validated_data.get(
            "no_reg_member", instance.no_reg_member
        )
        instance.id_poli = validated_data.get("id_poli", instance.id_poli)
        instance.id_faskes = validated_data.get("id_faskes", instance.id_faskes)
        instance.id_jadwal = validated_data.get("id_jadwal", instance.id_jadwal)
        instance.no_reg_dokter = validated_data.get(
            "no_reg_dokter", instance.no_reg_dokter
        )
        instance.tgl_kunjungan = validated_data.get(
            "tgl_kunjungan", instance.tgl_kunjungan
        )
        instance.jam_kunjungan = validated_data.get(
            "jam_kunjungan", instance.jam_kunjungan
        )
        instance.gejala = validated_data.get("gejala", instance.gejala)
        instance.status = validated_data.get("status", instance.status)
        instance.created_by = validated_data.get("created_by", instance.created_by)
        instance.is_created_by_staff = validated_data.get(
            "is_created_by_staff", instance.is_created_by_staff
        )
        if instance.status == "4":
            antrianInstance = TableAntrian.objects.get(id_admission=instance)
            antrianInstance.valid = False
            antrianInstance.nomerantrian = 0
            antrianInstance.save()

        listantrian = TableAntrian.objects.filter(
            Q(id_jadwal=instance.id_jadwal) and Q(valid=True)
        )
        resetAntrian(listantrian)
        
        instance.save()
        return instance


def resetAntrian(listAntrian):
    indexAntrian = 1
    for antrian in listAntrian:
        antrian.nomerantrian = indexAntrian
        antrian.save()
        indexAntrian += 1


class TableAntrianApi(serializers.ModelSerializer):
    nama_pasien = serializers.CharField(source="id_admission.no_reg_member.nama", read_only=True) 
    gejala = serializers.CharField(source="id_admission.gejala", read_only=True) 
    nama_dokter = serializers.CharField(source="id_jadwal.no_reg_dokter.nama", read_only=True) 
    poli = serializers.CharField(source="id_jadwal.id_poli.poli", read_only=True)
    admission_rawat_jalan_id = serializers.CharField(source="id_admission.admission_rawat_jalan_id", read_only=True)

    class Meta:
        model = TableAntrian
        fields = "__all__"

class TableObatApi(serializers.ModelSerializer):
    class Meta:
        model = TableObatPasien
        fields = ["nama_obat", "tgl_pemberian", "jenis_obat", "dosis"]