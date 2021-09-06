from django.http import request
from rest_framework import exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from user_management.models import TableBasicUser, TableUser, TableDokter
import datetime
import json
from django.contrib.auth import authenticate, login

class DokterTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, TableBasicUser):
        token = super(DokterTokenSerializer, cls).get_token(TableBasicUser)
        admin = TableDokter.objects.get(pk=TableBasicUser.id)
        # Add custom claims
        # token['lifetime'] = datetime.timedelta(days=15)
        token['username'] = admin.username
        token['id'] = admin.id
        token["no_reg_admin"] = admin.no_reg_dokter
        token["nama"] = admin.nama
        token["no_ktp"] = admin.no_ktp
        foto = admin.foto_identitas
        if foto:
            token["foto"] = foto.url
        return token

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
   
   