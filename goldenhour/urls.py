"""goldenhour URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from os import name
from django.contrib import admin
from django.urls import path, include
from rest_framework import views
from goldenhour import views
from .views import LoginUserTokenGenerator, LoginDokterTokenGenerator
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views_main
from pasien import page
urlpatterns = [
    path('', page.LoginPage, name='loginpage'),
    path('login/user/', LoginUserTokenGenerator.as_view(), name='token_obtain_pair'),
    path('login/dokter/', LoginDokterTokenGenerator.as_view(), name='token_dokter'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path('logout/all', views.logoutAll, name="logoutAll"),
    path('', include('user_management.urls')),
    path('dokter/', include('dokter.urls')),
    path('', include('admission_rawat_jalan.urls')),
    path('global/', include('globaldata.urls')),
    path('frontdesk/', include('frontdesk.urls')),
    path('pasien/', include('pasien.urls')),
    path('auth/login/', views.AuthSession, name="session-user"),

    # url(r'^$',views_main.index,name="Index"),
    # url(r'^cabinet-logout', views_main.cabinet_logout, name="CabinetLogout"),
    # url(r'^forgot-password/', views_main.forgotpassword, name="ForgotPassword"),
    url(r'^register-member', views_main.registermember, name="RegisterPassword"),
    # url(r'^edit-user', views_main.edituser, name="EditUser"),
    # url(r'^edit-profile', views_main.editprofile, name="EditProfile"),
    # url(r'^cabinet', views_main.cabinet, name="CabinetHome"),
    # url(r'^dokter', views_main.dokter, name="Dokter"),
    # url(r'^jadwal-utama', views_main.jadwalutama, name="JadwalUtama"),
    # url(r'^detail_user', views_main.detail_user, name="DetailUser"),
    # url(r'^change-password', views_main.change_password, name="ChangePassword"),
    # url(r'^list_faskes', views_main.list_faskes, name="ListFaskes"),
    # url(r'^list_doctor', views_main.list_doctor, name="ListDoctor"),
    # url(r'^register-rawat-jalan', views_main.register_rawat_jalan, name="RegisterRawatJalan"),
    # url(r'^view-calendar', views_main.view_calendar, name="ViewCalendar"),
    # url(r'^table-point', views_main.table_point, name="TablePoint"),
    # path('rawatjalan/<int:idrj>/',views_main.rawatjalan,name='ViewRawatJalan'),
    # path('gologin/<str:username>', views_main.go_login, name="CabinetLogin"),
    # path('register-success/<int:id>/',views_main.registersuccess,name='RegisterSuccess'),
    # url(r'^form-element', views_main.form_element, name="FormElement"),
]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
