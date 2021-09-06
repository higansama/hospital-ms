from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import BLANK_CHOICE_DASH
from goldenhour.helpers import *
from goldenhour import helpers
import time
# Create your models here.
SEKARANG = datetime.datetime.now()
BULAN = SEKARANG.strftime("%m")
TANGGAL = SEKARANG.strftime("%d")

class TableProvinsi(models.Model):
    id_provinsi = models.AutoField(primary_key=True)
    provinsi = models.CharField(max_length=100, blank=False, default="")

    def __str__(self):
        return str(self.id_provinsi) + " " + self.provinsi

    class Meta:
        pass

class TableKota(models.Model):
    id_kota = models.AutoField(primary_key=True)
    id_provinsi = models.ForeignKey(TableProvinsi, on_delete=models.CASCADE)
    kota = models.CharField(max_length=100, blank=False, default="")

    def __str__(self):
        return str(self.id_kota) + " " + self.kota

    class Meta:
        order_with_respect_to = "id_provinsi"

class TableKecamatan(models.Model):
    id_kecamatan = models.AutoField(primary_key=True)
    id_kota = models.ForeignKey(TableKota, on_delete=models.CASCADE)
    kecamatan = models.CharField(max_length=100, blank=False, default="")

    def __str__(self):
        return str(self.id_kecamatan) + " " + self.kecamatan



class TableKelurahan(models.Model):
    id_kelurahan = models.AutoField(primary_key=True)
    id_kecamatan = models.ForeignKey(TableKecamatan, on_delete=models.CASCADE)
    kelurahan = models.CharField(max_length=100, blank=False, default="")

    def __str__(self):
        return str(self.id_kelurahan) + " " + self.kelurahan        


class TableFaskes(models.Model):
    id_faskes = models.AutoField(primary_key=True)
    faskes = models.CharField(max_length=32)
    alamat = models.CharField(max_length=100, default="")
    status_faskes = models.CharField(default="1", max_length=1)
    status_asuransi = models.CharField(default="0", max_length=1)
    kelurahan = models.ForeignKey(TableKelurahan, on_delete=models.CASCADE,blank=True, null=True)
    def __str__(self):
        return self.faskes

class TablePoli(models.Model):
    id = models.AutoField(primary_key=True)
    id_faskes = models.ForeignKey(TableFaskes, blank=True, null=True, on_delete=models.CASCADE)
    poli = models.CharField(max_length=50, blank=False)
    status = models.BooleanField(default=False)

    def __str__(self):
        status = "Tidak Aktif"
        if self.status == True:
            status = "Aktif"
        return str(self.id) + " |  " + self.poli + " " + status 
    
    class Meta:
        pass




class TableDivisi(models.Model):
    id_divisi = models.AutoField(primary_key=True)
    divisi = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return str(self.id_divisi) + " | " + self.divisi

class TableBasicUser(AbstractUser):
    no_telepon = models.CharField(max_length=100, blank=True)
    no_ponsel = models.CharField(max_length=100, blank=True)
    tingkat_pendidikan = models.CharField(max_length=100, blank=False, default="")
    kodepos_utama = models.CharField(max_length=5, null=False, blank=True, default="")
    kodepos_domisili = models.CharField(max_length=5, blank=True, default="")
    alamat_utama = models.TextField(null=False, blank=False, default="")
    alamat_domisili = models.TextField(blank=False, default="")
    kelurahan_utama = models.ForeignKey(TableKelurahan, on_delete=models.CASCADE, related_name="kelurahanutama", null=True)
    kecamatan_utama = models.ForeignKey(TableKecamatan, on_delete=models.CASCADE, related_name="kecamatanutama", null=True)
    kota_utama = models.ForeignKey(TableKota, on_delete=models.CASCADE, related_name="kotautama", null=True)
    provinsi_utama = models.ForeignKey(TableProvinsi, on_delete=models.CASCADE, related_name="provinsiutama", null=True)
    kelurahan_domisili = models.ForeignKey(TableKelurahan, on_delete=models.CASCADE, related_name="kelurahandomisili", null=True)
    kecamatan_domisili = models.ForeignKey(TableKecamatan, on_delete=models.CASCADE, related_name="kecamatandomisili", null=True)
    kota_domisili = models.ForeignKey(TableKota, on_delete=models.CASCADE, related_name="kotadomisili", null=True)
    provinsi_domisili = models.ForeignKey(TableProvinsi, on_delete=models.CASCADE, related_name="provinsidomisili", null=True)
    tempat_lahir = models.CharField(max_length=100, blank=True, default="")
    tgl_lahir = models.DateField(blank=True, null=True)
    jenis_kelamin = models.BooleanField(default=True) # laki - laki = true
    no_asuransi = models.CharField(max_length=50, blank=True)
    status_keanggotaan = models.BooleanField(default=False)
    foto_identitas = models.ImageField(upload_to="foto/profile/", blank=True, default="/default-profile.jpg")
    inisial = models.CharField(max_length=20, blank=True, default="")
    jenis_anggota = models.SmallIntegerField(default=4) 
    def __str__(self):
        return self.first_name + " " + self.last_name + " " +self.username

class TableUser(TableBasicUser):
    nama = models.CharField(max_length=100, blank=False, unique=False)
    no_reg_member = models.CharField(max_length=100, default="0", blank=False, unique=True)
    profesi = models.CharField(max_length=100, blank=True)
    no_ktp = models.CharField(max_length=100, null=True, unique=False)
    
    def __str__(self):
        return "Pasien " + self.no_ktp + " " +self.username

class TableUserKeluarga(TableUser):
    hubungan_keluarga = models.CharField(max_length=100, blank=False) #anak, istri, dl
    parent = models.CharField(max_length=30, blank=True)
    profile_updated = models.BooleanField(default=False)
    password_updated = models.BooleanField(default=False)

    def __str__(self):
        # namaparent = TableUser.objects.get(pk=self.parent).username
        return "nama = %s | parent = %s" % (self.nama, self.parent ) 


class TableDokter(TableBasicUser):
    no_ktp = models.CharField(max_length=100, null=False, unique=True, default=IDGenerator())
    nama = models.CharField(max_length=100, blank=False, unique=False)
    no_reg_dokter = models.CharField(max_length=100, unique=True)
    id_poli = models.ForeignKey(TablePoli, on_delete=models.CASCADE, blank=True)
    id_faskes = models.ForeignKey(TableFaskes, on_delete=models.CASCADE, blank=True,related_name="dokters")
    
    def __str__(self):
        return "dr " + self.username + " " + self.no_reg_dokter
        

class TablePerawat(TableBasicUser):
    no_ktp = models.CharField(max_length=100, null=False, unique=True, default=IDGenerator())
    nama = models.CharField(max_length=100, blank=False, unique=False)
    no_reg_perawat = models.CharField(max_length=100, unique=True)
    id_poli = models.ForeignKey(TablePoli, on_delete=models.CASCADE)
    id_faskes = models.ForeignKey(TableFaskes, on_delete=models.CASCADE)
    def __str__(self):
        return "suster " + self.username

class TableAdmin(TableBasicUser):
    no_ktp = models.CharField(max_length=100, null=False, unique=True, default=IDGenerator())
    nama = models.CharField(max_length=100, blank=False, unique=False)
    no_reg_admin = models.CharField(max_length=100, blank=False, unique=False)
    divisi_id = models.ForeignKey(TableDivisi, on_delete=models.CASCADE, blank=True, null=True)
    id_faskes = models.ForeignKey(TableFaskes, on_delete=models.CASCADE, blank=True, null=True)
    gh_admin = models.BooleanField(default=False)

    def __str__(self):
        return "%s " % (self.username)

class TableLogPointUser(models.Model):
    id = models.AutoField(primary_key=True,)
    no_reg_member = models.CharField(max_length=100, null=True, blank=True)
    get_point = models.IntegerField(default=0)
    minus_point = models.IntegerField(default=0)
    total_point = models.IntegerField(default=0)
    service = models.CharField(max_length=100, default="", blank=True, null=True)
    date_created = models.DateTimeField(auto_created=True, auto_now=True)
    
    def __str__(self): 
        return str(self.total_point) + " " + self.no_reg_member

    class Meta:
        ordering = ["id"]
        get_latest_by = ['date_created']

class TableLogPointDokter(models.Model):
    id = models.AutoField(primary_key=True,)
    no_reg_dokter = models.CharField(max_length=100, default="0", blank=True)
    get_point = models.IntegerField(default=0)
    minus_point = models.IntegerField(default=0)
    total_point = models.IntegerField(default=0)
    service = models.CharField(max_length=100, default="", blank=True, null=True)
    date_created = models.DateTimeField(auto_created=True, auto_now=True)
    
    def __str__(self): 
        return str(self.get_point) + " " + self.no_reg_dokter


    class Meta:
        ordering = ["date_created"]



class TableRekamMedis(models.Model):
    id = models.AutoField(primary_key=True)
    no_rekam_medis = models.CharField(max_length=32, null=False, default="")
    tindakan_pengobatan = models.TextField(blank=True)
    diagnosa = models.TextField(blank=True)
    no_reg_dokter = models.ForeignKey(TableDokter, on_delete=models.CASCADE, blank=True, null=True)
    no_reg_member = models.ForeignKey(TableUser, on_delete=models.CASCADE, blank=True)
    tgl_pengobatan = models.DateField(null=True, blank=True)
    id_admission = models.CharField(max_length=32, blank=True, null=True)
    
    def __str__(self):
        return "%s | %s" % (self.no_rekam_medis, self.no_reg_member)
    
