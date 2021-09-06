# from user_management.viewsapi import RekamMedisClass
from os import name
from django.urls import path, include
from . import views
from . import page
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
# router.register(r'pasien', viewsapi.PasienClass)
# router.register(r'poli', viewsapi.PoliClass)
# router.register(r'', viewsapi.FaskesClass)
# router.register(r'divisi', viewsapi.DivisiClass)

urlpatterns = [
    path("account/list", views.PasienClass.as_view()),
    path("account/detail/", views.PasienUpdateClass.as_view()),
    path("account/detail/ue", views.UpdateUsernameDanEmail),
    path("update/password/", views.UpdatePassword),
    path("account/upload/poto", views.PasienUploadPoto.as_view()),
    path("rekammedis", views.RekamMedisClass.as_view()),
    path("rekammedis/detail/<int:id>", views.RekamMedisClassDetail,),
    path(
        "rawatjalan/list/",
        views.PasienAdmission.as_view(),
    ),
    path(
        "rawatjalan/checkin/<str:idadmision>/",
        views.PasienCheckin.as_view(),
    ),
    path(
        "rawatjalan/update/<str:idadmision>/",
        views.PasienAdmissionUpdate.as_view(),
    ),
    path(
        "points/<str:jenis>",
        views.PointPasien.as_view(),
    ),
    path("rawatjalan/cancel/<str:id>", views.CancelRawatJalan),
    # keluarga
    path("keluarga/", views.KeluargaClass.as_view()),

    path("faskes/<str:kota>", views.GetFaskes.as_view()),
    path("faskes/detail/<str:idfaskes>", views.DetailFaskes.as_view()),

    # get dokter by poli after today
    path('list/jadwal/dokter/<str:idpoli>/<str:hari>/', views.GetDokterByIDPoli.as_view()),
    path('detail/jadwal/dokter', views.DetailJadwalDokter, name="detailjadwaldokter" ),
    path('list/jadwal/dokter/byid/<str:iddokter>', views.GetJadwalDokterByID.as_view()),
    
    # Page
    path('login', page.LoginPage, name="loginpasien"),
    path('logout', page.LogoutProses, name="logoutpasien"),
    path('home', page.Dashboard, name="home"),
    path('rawatjalan', page.RawatJalan, name="pagerawatjalan"),
    path('faskes', page.FaskesPage, name="faskes"),
    path('faskes/poli/page', page.PoliPage, name="polipage"),
    path('profile/old', page.PasienProfileOld, name="profileold"),
    path('profile', page.PasienProfile, name="profile"),
    path('profile/edit', page.EditProfile, name="editprofile"),
    path('profile/family', page.FamilyPage, name="familypage"),
    path('register', page.SignUpPage, name="signuppage"),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)