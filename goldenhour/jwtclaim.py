from django.http import request
from rest_framework import exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from user_management.models import TableUser, TableDokter, TableBasicUser
import datetime
import json
from django.contrib.auth import authenticate, login

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        req_context = self.context['request']
        # print(req_context.data['username'])
        iusername = req_context.data['username']
        ipassword = req_context.data['password']
        try:
            user = authenticate(username=iusername, password=ipassword)
            login(req_context, user)
        except:
            error_message = "Username or Password is not match"
            error_name = "Login Failed"
            raise exceptions.AuthenticationFailed(error_message, error_name)
        return super().validate(attrs)
   
    @classmethod
    def get_token(cls, TableBasicUser):
        token = super(MyTokenObtainPairSerializer, cls).get_token(TableBasicUser)
        # Add custom claims
        # token['lifetime'] = datetime.timedelta(days=15)
        token['username'] = TableBasicUser.username
        token['id'] = TableBasicUser.id
        pasien = TableUser.objects.get(pk=TableBasicUser.id)
        token["nama"] = pasien.nama
        token["no_reg_member"] = pasien.no_reg_member
        token["profesi"] = pasien.profesi
        token["no_ktp"] = pasien.no_ktp
        token["jenis_anggota"] = pasien.jenis_anggota
        foto = pasien.foto_identitas
        if foto:
            token["foto"] = foto.url
        else:
            token["foto"] = ""

        return token

class DokterJWTSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['username'] = user.username
        token['id'] = user.id
        token['dokter'] = TableDokter.objects.get(pk=user.id)
        return token