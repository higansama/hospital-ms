from django.urls import path, include
from . import views, viewsapi, viewsdokter
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
# router.register(r'pasien', viewsapi.PasienClass)
router.register(r'poli', viewsapi.PoliClass)
router.register(r'', viewsapi.FaskesClass)
router.register(r'divisi', viewsapi.DivisiClass)

urlpatterns = [
    path('account/user/list',viewsapi.PasienClass.as_view()),
    path('account/user/update/<str:idpasien>',viewsapi.PasienUpdateClass.as_view()),
    # path('user/rekammedis/<str:tahun>/<str:bulan>/<str:tanggal>/<str:index>', viewsapi.RekamMedisClass.as_view()),
    # path('faskes/', include(router.urls)),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# urlpatterns = [
    # path('divisi/all', viewsapi.DivisiClass.as_view()),
    # path('', views.Test, name="test"),
    # path('account/user/registrasi', views.UserRegister, name="pasien-regist"),
    # path('account/perawat/', views.PerawatRegister, name="docter-regist"),
    # path('account/dokter/registrasi', views.DocterRegister, name="docter-regist"),
    # path('account/dokter/', views.DocterRegister, name="docter-all"),
    # path('account/dokter/points/<str:nama_faskes>/dokter/<str:tahun>/<str:bulan>/<str:tgl>/<str:no_urut>', views.DocterPoint, name="docter-points"), 
    # path('account/dokter/add/rekammedis', views.SaveRekamMedis, name="tambah-rekam-medis"),
    # path('account/staff/registrasi', views.StaffRegister, name="staff-regist"),
    # path('account/staff/', views.StaffRegister, name="staff-all"),
    # path('account/user/', views.UserRegister, name="pasien-regist"),
    # path('account/user/family', views.Family, name="pasien-regist"),
    # path('account/user/family/<str:tahun>/<str:bulan>/<str:tanggal>/<str:index>/', views.FamilyList, name="point"),
    # path('account/user/point/<str:tahun>/<str:bulan>/<str:tanggal>/<str:index>/', views.PointUser, name="point"),
    # path('account/user/rekammedis/<str:tahun>/<str:bulan>/<str:tanggal>/<str:index>/', views.RekamMedis, name="rekammedisuser"),

    # faskes dd
    # path('faskes/', viewsapi.Faskes, name="faskesapi"),
    # path('profile/',)
# ]