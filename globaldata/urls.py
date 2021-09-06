
from django.urls import path, include
from globaldata import views
# from globaldata.views import GetPoliByFaskes
from pasien.views import GetFaskes as FaskesPasien
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'provinsi', views.ProvinsiClass)


urlpatterns = [
    path('', include(router.urls)),
    path('kota/', views.KotaController),
    path('kecamatan/', views.KecamatanKontroller),
    path('kelurahan/', views.KelurahanKontoler),
    path('cari/kelurahan/', views.CariKelurahan),
    # get faskes by kota
    path('faskes/<str:kota>', FaskesPasien.as_view(), name="get-faskes-perkota"),
    # get poli by faskes
    path('poli/<str:idfaskes>', views.GetPoliByFaskes.as_view(), name="get-poli-byfaskes"),
    # get faskes, poli, dokter, tanggal, jam[important] yang terisi based on tanggal
    path('faskes/detail/<str:idfaskes>', views.FaskesDetail, name="detail-faskes")

    # path('provinsi/', views.Provinsi, name="show-provinsi"),
]