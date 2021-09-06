from re import split
from django.core import serializers
import string
import random
import datetime
import jwt
from django.http import JsonResponse
from random import choice

from rest_framework.fields import JSONField

SEKARANG = datetime.datetime.now()
BULAN = SEKARANG.strftime("%m")
TANGGAL = SEKARANG.strftime("%d")
TAHUN = SEKARANG.strftime("%G")
NAMAHARI = SEKARANG.strftime("%A")


def IDGenerator(size=6, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def RandomUsername(size):
    randomstring = [random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(3)]
    return ''.join(randomstring)

def usernameGenerator(nama, nohp):
    username = split(" ", nama.lower())
    if len(username) > 1:
        username =  username[0] + nohp[-4:] + RandomUsername(3)
    else:
        username = nama + nohp[-4:] + RandomUsername(3)
    return username    
    

def jsonReturn(code, message, data):
    data = {
        "message": message,
        "code": 200,
        "data": data,
    }
    return data


def FailReturn(exceptionObj):
    data = {"data": [], "code": 500, "message": str(exceptionObj)}


def SerializeData(data):
    r = serializers.serialize("JSON", data)
    return r


def abbreviator(kalimat):
    s = ''.join([x[0].upper() for x in kalimat.split(' ')])
    return s


def jabatanGen(kodejabatan):
    if kodejabatan == 1:
        return "pasien"
    elif kodejabatan == 2:
        return "dokter"
    elif kodejabatan == 3:
        return "perawat"
    elif kodejabatan == 4:
        return "staff"
    elif kodejabatan == 5:
        return "anggota keluarga"
    else:
        return None


def RegistrationCodeGeneratorFamily(counted_id):
    noregis = ""
    sekarang = datetime.datetime.now()
    bulan = sekarang.strftime("%m")
    tanggal = sekarang.strftime("%d")
    tahun = sekarang.strftime("%G")
    # No reg user : tahun/bulan/tgl/no_urut, misal 2021/04/06/00001
    noregis = ("%s/FAM/%s/%s/%s") % (tahun, bulan, tanggal, counted_id + 1)
    return noregis

def RegistrationPasienGenerator(jabatan, objData):
    noregis = ("%s/%s/%s/%s/%s") % (
            TAHUN,
            BULAN,
            TANGGAL,
            "staff",
            ReturnZeroGenerator(objData.count() + 1),
    )
    return noregis

def RegistrationStaff(countdata, namafaskes):
    nourut = 0

    if countdata == 0:
        nourut = 1
    else:
        nourut = countdata + 1

    nourut = ReturnZeroGenerator(nourut)
    noregis = ("%s/%s/%s/%s/%s") % (
        abbreviator(namafaskes),
        TAHUN,
        BULAN,
        TANGGAL,
        nourut,
    )
    return noregis

def RegistrationCodeGenerator(jabatan, objData, countData, namafaskes=""):
    reset = False
    if objData is None:
        reset = True
    else:
        reset = DokterCountedIDGenerator(objData)
    nourut = 0

    if countData == 0 or reset == True:
        nourut = 1
    else:
        nourut = countData + 1

    nourut = ReturnZeroGenerator(nourut)
    if jabatan != 3:
        # No reg dokter: nama_faskes/dokter/tahun/bulan/tgl/no_urut, misal klinik kimia farma menjadi KF/staff/2021/04/06/00001
        # No reg perawat: nama_faskes/dokter/tahun/bulan/tgl/no_urut, misal klinik kimia farma menjadi KF/staff/2021/04/06/00001
        # No reg admin: nama_faskes/staff/tahun/bulan/tgl/no_urut, misal klinik kimia farma menjadi KF/staff/2021/04/06/00103
        noregis = ("%s/%s/%s/%s/%s/%s") % (
            abbreviator(namafaskes),
            jabatanGen(jabatan),
            TAHUN,
            BULAN,
            TANGGAL,
            nourut,
        )
        return noregis
    else:
        # No reg user : tahun/bulan/tgl/no_urut, misal 2021/04/06/00001
        noregis = ("%s/%s/%s/%s") % (
            tahun,
            bulan,
            tanggal,
            nourut,
        )
        return noregis


def DokterCountedIDGenerator(data):
    noreg = data.no_reg_dokter.split("/")
    pastdate = datetime.datetime(int(noreg[2]), int(noreg[3]), int(noreg[4]))
    reset = SEKARANG < pastdate
    return reset


def ReturnZeroGenerator(nourut):
    strurut = str(nourut)
    if len(strurut) == 1:
        strurut = "00000" + strurut
    elif len(strurut) == 2:
        strurut = "0000" + strurut
    elif len(strurut) == 3:
        strurut = "000" + strurut
    elif len(strurut) == 4:
        strurut = "00" + strurut
    elif len(strurut) == 5:
        strurut = "0" + strurut
    return strurut


def RekamMedisGenerator(user, rm):
    inisial = abbreviator(user.nama)
    print("inisial =>", inisial)
    # formatnya rekammedis/inisial_nama_pasien/no_urut, misal RM/TMK/00001
    if rm.count() > 1:
        return "RM/" + inisial + "/" + str(ReturnZeroGenerator(rm.count() + 1))
    else:
        return "RM/" + inisial + "/" + "00001"


def AdmissionRawatJalanGenerator(objData, namafaskes):
    # No admission rawat jalan : nama_faskes/RJ/tahun/bulan/tgl/no_urut, misal klinik kimia farma menjadi KF/RJ/2021/04/06/00001
    nourut = ReturnZeroGenerator(objData.count() + 1)
    print(nourut)
    return abbreviator(namafaskes)+ "/RJ/"+ TAHUN+ "/" + BULAN + "/" + TANGGAL + "/" + nourut

# def GetNextNumber(objData, )

def JWTDecoder(request):
    token = request.META['HTTP_AUTHORIZATION'].split(' ')
    return jwt.decode(token[1], "*!1pq@$j3i5x&ixr5de($z7)*-d5dm19$xwi01g0uau7zcl*e2", 'HS256')

def HariIniBahasa(day):
    hari = ""
    if day == "sunday": 
        hari = "Minggu"
    if day == "Monday":
        hari = "Senin"
    if day == "Tuesday":
        hari = "Selasa"
    if day == "Wednesday":
        hari = "Rabu"
    if day == "Thursday":
        hari = "Kamis"
    if day == "Friday":
        hari = "Jumat"
    if day == "Saturday":
        hari = "Sabtu"

