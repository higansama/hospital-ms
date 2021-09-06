from django.urls import path, include
from frontdesk.views import *
from rest_framework import routers
from . import pages
from . import views 

router = routers.DefaultRouter()
router.register(r'account', FrontDeskClass)
router.register(r'faskes/api', FaskesAdmin)

urlpatterns = [
    path('loginproses/', LoginProcess.as_view(), name="loginprosesfd"),
    path('logoutproses/', pages.LogoutProses, name="fdlogoutproses"),
    # path('',include(FrontDesk.urls)),
    path('', include(router.urls)),
    path('profile/', FrontDeskDetail.as_view()),
    path('rawatjalan/api', FrontdeskRawatJalan.as_view()),
    path('add/jadwal/dokter/<str:iddokter>', DokterJadwal.as_view()),
    path('rawatjalan/<str:idstaff>/<str:idfaskes>', FrontdeskRawatJalan.as_view()),
    path('rawatjalan/checkin/<str:idstaff>/<str:idfaskes>/<str:idrawatjalan>/<str:statusparam>', CheckinRawatJalan.as_view()),
    path('dokter/list/<str:idfaskes>/<str:idpoli>', views.GetDokterByFaskesDanPoli, name="listDokterByPoli"),
    path('checkin/pasien/<str:idantrian>', views.CheckinPasien),
    path('checkin/dokter/<str:idjadwal>', views.checkinDokter),
    path('jadwal/utama/dokter/<str:idpoli>', views.getJadwalPraktekDokter),
    # path('rawatjalan/detail/<int:pk>', FrontdeskRawatJalanDetail().as_view()),
    # tambah rawat jalan

    path('login/', pages.LoginPage, name="frontdeskloginpage"),
    path('dashboard/', pages.Dashboard, name="fddashboard"),
    path('faskes/', pages.Faskes, name="fdfaskes"),
    path('rawatjalan/', pages.RawatJalan, name="fdrawatjalan"),
    path('jadwal/dokter/', pages.JadwalDokter, name="jadwalDokter"),
    path('dokter/', pages.HalamanDokter, name="halamanDokter"),
    path('list/antrian/<str:idjadwal>/<str:titimangsa>', views.AntrianByID),
    path('faskes/<str:idfaskes>', pages.DetailFaskes, name="detailfaskes"),
    # API
    path('rawatjalan/otomatis/', views.AddRawatJalanOtomatis, name="otomatisrawatjalan")
]