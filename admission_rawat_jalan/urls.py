from django.urls import path, include
from admission_rawat_jalan.views import JadwalPraktekClass, PraktekDokterClass, TableAdmissionClass
from rest_framework import routers

admision = routers.DefaultRouter()
# admision.register(r'admission', TableAdmissionClass)
admision.register(r'jadwal', JadwalPraktekClass)
admision.register(r'', PraktekDokterClass)
urlpatterns = [
    path('praktek/', include(admision.urls)),
    path('pasien/admission/', TableAdmissionClass.as_view()),
    # path('rawat/jalan/', TableAdmissionClass.as_view())
]