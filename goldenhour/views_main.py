from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import os
from pathlib import Path
from localStoragePy import localStoragePy
from user_management.models import *

def index(request):
    #isi = {'title' : 'Sundareka - Goldenhour'}
    basedir = BASE_DIR = Path(__file__).resolve().parent.parent
    con = {'BASE_DIR':basedir,
           'title' : 'Login Page'
          }
    return render(request,'django_index.html',con,content_type = 'text/html')

def forgotpassword(request):
    con = {
           'title' : 'Forgot Password'
          }
    return render(request,'django_page_forgot_password.html',con,content_type = 'text/html')

def registermember(request):
    con = {
           'title' : 'Register Member'
          }
    return render(request,'django_register.html',con,content_type = 'text/html')

def edituser(request):
    datauser = {
        'name' : 'Rian Hariadi'
    }
    con = {
           'user' : datauser
          }
    return render(request,'django_edit_user.html',con,content_type = 'text/html')

def editprofile(request):
    con = {
           'title' : 'Register Member'
          }
    return render(request,'django_edit_profile.html',con,content_type = 'text/html')


def go_login(request,username):
    storage = localStoragePy('goldenhour2', 'json')
    storage.setItem('usernamelogin',username)
    return HttpResponseRedirect('/cabinet')


def cabinet(request):
    token = localStoragePy('token');
    islogin= localStoragePy('goldenhour', 'json')
    islogin.setItem('islogin',1)
    localStorage = localStoragePy('goldenhour2', 'json')
    username = localStorage.getItem('usernamelogin')
    datauser = TableBasicUser.objects.filter(username=id).values()
    con = {
           'title' : 'Register Member',
            'token' : username,
          }
    return render(request,'django_cabinet.html',con,content_type = 'text/html')


def cabinet_logout(request):
    localStorage = localStoragePy('goldenhour', 'json')
    localStorage.setItem('islogin', 0)
    return HttpResponseRedirect('/')




def dokter(request):
    con = {
           'title' : 'Dokter Cabinet'
          }
    return render(request,'django_dokter_cabinet.html',con,content_type = 'text/html')



def list_faskes(request):
    localStorage = localStoragePy('goldenhour', 'json')
    check = localStorage.getItem('islogin')
    if (check == '1'):
        lanjut = 1
    else:
        lanjut = 0

    if (lanjut == 0):
        return HttpResponseRedirect('/')

    con = {
           'title' : lanjut
          }
    return render(request,'django_list_faskes.html',con,content_type = 'text/html')

def list_doctor(request):
   pass

def table_point(request):
    con = {
           'title' : 'Table Point'
          }
    return render(request,'django_table_point.html',con,content_type = 'text/html')



def register_rawat_jalan(request):
    con = {
           'title' : 'Register Rawat Jalan'
          }
    return render(request,'django_register_rawatjalan.html',con,content_type = 'text/html')

def view_calendar(request):
    con = {
           'title' : 'Register Rawat Jalan'
          }
    return render(request,'django_view_calendar.html',con,content_type = 'text/html')


def detail_user(request):
    con = {
           'title' : 'Register Member'
          }
    return render(request,'django_detail_user.html',con,content_type = 'text/html')

def change_password(request):
    con = {
           'title' : 'Change Password'
          }
    return render(request,'django_change_password.html',con,content_type = 'text/html')


def form_element(request):
    con = {
           'title' : 'Register Member'
          }
    return render(request,'django_form-element.html',con,content_type = 'text/html')



def registersuccess(request,id):
    data = TableBasicUser.objects.filter(id = id).values()
    data = data[0]
    con = {
        "user" : data
    }
    return render(request, 'django_registersuccess.html', con, content_type='text/html')


def rawatjalan(request,idrj):
    status = 0
    if (idrj == 122):
        status = 0
        notif = ''
    if (idrj == 123):
        status = 2
        notif = ''
    if (idrj == 124):
        status = 2
        notif = ''
    if (idrj == 125):
        status = 1
        notif = '<span style="color: red">Dokter telah membatalkan kunjungan ini. Silahkan cancel atau ubah jadwal kujungan ini..' \
                'Anda tidak mendapat pengurangan point untuk ini. ' \
                'Dokter ini tidak bisa praktik di hari kunjungan yang Anda pilih. Jadwal Anda digeser ke jadwal dokter di hari lain. </span>'



    con = {
        'title' : 'Log Rawat Jalan',
        'idrj'  : idrj,
        'status' : status,
        'notif' : notif
    }
    return render(request,'django_rawatjalan.html',con,content_type = 'text/html')


def jadwalutama(request):
    con = {
           'title' : 'Table Jadwal Utama'
          }
    return render(request,'django_register_jadwalutama.html',con,content_type = 'text/html')

def registersuccess(request,id):
    data = TableBasicUser.objects.filter(id = id).values()
    data = data[0]
    con = {
        "user" : data
    }

    return render(request, 'django_registersuccess.html', con, content_type='text/html')
