from django.contrib import admin
from user_management.models import *

# Register your models here.


class TableUserAdmin(admin.ModelAdmin):
    # fields = ("no_ktp","nama_depan","nama_belakang","no_telepon","no_ponsel","profesi","tingkat_pendidikan","alamat_utama","kelurahan_utama","kecamatan_utama","kota_utama","kodepos_utama","provinsi_utama","alamat_domisili","alamat_domisili","kelurahan_domisili","kecamatan_domisili","kota_domisili","kodepos_domisili","provinsi_domisili","tempat_lahir","tgl_lahir","jenis_kelamin","no_asuransi","status_keanggotaan","foto_identitas")
    pass


class TableAdminAdmin(admin.ModelAdmin):
    # fields = ("no_ktp","nama_depan","nama_belakang","no_telepon","no_ponsel","profesi","tingkat_pendidikan","alamat_utama","kelurahan_utama","kecamatan_utama","kota_utama","kodepos_utama","provinsi_utama","alamat_domisili","alamat_domisili","kelurahan_domisili","kecamatan_domisili","kota_domisili","kodepos_domisili","provinsi_domisili","tempat_lahir","tgl_lahir","jenis_kelamin","no_asuransi","status_keanggotaan","foto_identitas")
    pass


class TableDokterAdmin(admin.ModelAdmin):
    fields = ("no_ktp", "no_reg_dokter", "id_poli", "id_faskes", "nama", "username")


class PoliAdmin(admin.ModelAdmin):
    fields = ("poli", "status", "id_faskes")


class FaskesAdmin(admin.ModelAdmin):
    fields = ["faskes", "kelurahan", "status_faskes"]


class DivisiAdmin(admin.ModelAdmin):
    fields = ["divisi"]


class TableProvinsiAdmin(admin.ModelAdmin):
    fields = ["provinsi"]


class TableKotaAdmin(admin.ModelAdmin):
    fields = ["id_provinsi", "kota"]


class TableKecamatanAdmin(admin.ModelAdmin):
    fields = ["id_kota", "kecamatan"]


class TableKelurahanAdmin(admin.ModelAdmin):
    fields = ["id_kecamatan", "kelurahan"]


admin.site.register(TableUser, TableUserAdmin)
admin.site.register(TableAdmin, TableAdminAdmin)
admin.site.register(TableDokter, TableDokterAdmin)
admin.site.register(TablePoli, PoliAdmin)
admin.site.register(TableFaskes, FaskesAdmin)
admin.site.register(TableDivisi, DivisiAdmin)
admin.site.register(TableProvinsi, TableProvinsiAdmin)
admin.site.register(TableKota, TableKotaAdmin)
admin.site.register(TableKecamatan, TableKecamatanAdmin)
admin.site.register(TableKelurahan, TableKelurahanAdmin)
