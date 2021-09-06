from django.urls import path, include
from dokter.views import *
from . import views
from rest_framework import routers

routerDokter = routers.DefaultRouter()
routerDokter.register(r'', DokterClass)

urlpatterns = [
    path('', include(routerDokter.urls)),
    # dokter/detail/ [token]
    path('login/proses/', DokterTokenSerializer.as_view(), name="dokterlogin"),
    path('detail/profile/', DetailDokter.as_view()),
    path('points/<str:jenis>', DokterPoints.as_view()),
    path('jadwal/<str:id>', DokterJadwal.as_view()),
    path('kunjungan/pasien/<str:idkunjungan>', views.KunjunganDokter),
    path('kunjungan/', DokterKunjungan.as_view()),
    path('kunjungan/konfirmasi/<str:idkunjungan>/<str:statuskunjungan>', DokterKonfirmasiKunjungan.as_view()),
    path('diagnosa/<str:iduser>', DokerDiagnosa.as_view())
]