from django.db import models
from django.db.models.fields import DateField
from user_management.models import * 
# Create your models here.


class TableJadwalPraktekDokter(models.Model):
    id = models.AutoField(primary_key=True)
    no_reg_dokter = models.ForeignKey(TableDokter, on_delete=models.DO_NOTHING)
    id_poli = models.ForeignKey(TablePoli, on_delete=models.DO_NOTHING)
    id_faskes = models.ForeignKey(TableFaskes, on_delete=models.DO_NOTHING)
    jadwal_praktek = models.CharField(max_length=10, blank=True) # hari
    jam_mulai = models.CharField(max_length=10, blank=True)
    jam_selesai = models.CharField(max_length=10, blank=True)
    status_jadwal = models.BooleanField(default=False)
    def __str__(self):
        return str(self.id) + " " + self.no_reg_dokter.nama

class AdmissionRawatJalan(models.Model):
    # sini
    id = models.AutoField(primary_key=True)
    admission_rawat_jalan_id = models.CharField(max_length=100, unique=True, default="")
    no_reg_member = models.ForeignKey(TableUser, on_delete=models.DO_NOTHING, related_name="noregmember")
    id_poli = models.ForeignKey(TablePoli, on_delete=models.DO_NOTHING)
    id_faskes = models.ForeignKey(TableFaskes, on_delete=models.DO_NOTHING)
    id_jadwal = models.ForeignKey(TableJadwalPraktekDokter, on_delete=models.DO_NOTHING, blank=True)
    no_reg_dokter = models.ForeignKey(TableDokter, on_delete=models.CASCADE)
    tgl_kunjungan = models.DateField()
    jam_kunjungan = models.TimeField()
    gejala = models.TextField()
    status = models.CharField(max_length=2, default="1")
    created_by = models.CharField(max_length=100, blank=True)
    is_created_by_staff = models.BooleanField(default=False)
    date_created = DateField(blank=True, auto_created=True, auto_now_add=True)
    def __str__(self):
        return self.admission_rawat_jalan_id

class TableKunjunganDokter(models.Model):
    id = models.AutoField(primary_key=True)
    no_reg_dokter = models.ForeignKey(TableDokter, on_delete=models.DO_NOTHING)
    id_jadwal = models.ForeignKey(TableJadwalPraktekDokter, on_delete=models.DO_NOTHING)
    jumlah_pasien = models.IntegerField(default=0)
    status_jadwal = models.SmallIntegerField(default=0, blank=True)
    checkin_date = models.DateTimeField(auto_now_add=True)
    checkout_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "Praktek Dokter " + str(self.id) + "| " + self.no_reg_dokter.nama

class TableAntrian(models.Model):
    id = models.AutoField(primary_key=True)
    id_jadwal = models.ForeignKey(TableJadwalPraktekDokter, blank=True, null=True, on_delete=models.SET_NULL)
    id_admission = models.ForeignKey(AdmissionRawatJalan, on_delete=models.DO_NOTHING)
    status_checkin = models.BooleanField(default=False)
    tanggal_checkin = models.DateTimeField(default="2000-01-01 00:00")
    nomerantrian = models.IntegerField(blank=True)
    valid = models.BooleanField(default=True)
    def __str__(self):
        return str(self.id) + " " + self.id_admission.no_reg_member.username + " " + str(self.nomerantrian)

class TableObatPasien(models.Model):
    id_obat_passien = models.AutoField(primary_key=True)
    id_admission_rawat_jalan = models.ForeignKey(AdmissionRawatJalan, on_delete=models.DO_NOTHING)
    no_reg_member = models.ForeignKey(TableBasicUser, on_delete=models.DO_NOTHING, related_name="obatmember")
    no_reg_dokter = models.ForeignKey(TableDokter, on_delete=models.DO_NOTHING, related_name="obatdokter")
    tgl_pemberian = models.DateTimeField()
    jenis_obat = models.CharField(max_length=100)
    nama_obat = models.CharField(max_length=100)
    dosis = models.CharField(max_length=50)

    def __str__(self):
        return self.nama_obat + " " + self.dosis 
