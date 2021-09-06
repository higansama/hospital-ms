from django.http import request
from rest_framework import exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from user_management.models import TableBasicUser, TableUser, TableAdmin
import datetime
import json
from django.contrib.auth import authenticate, login

class AdminTokenSerializer(TokenObtainPairSerializer):

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
        token = super(AdminTokenSerializer, cls).get_token(TableBasicUser)
        admin = TableAdmin.objects.get(pk=TableBasicUser.id)
        # Add custom claims
        # token['lifetime'] = datetime.timedelta(days=15)
        token['username'] = admin.username
        token['id'] = admin.id
        token["no_reg_admin"] = admin.no_reg_admin
        token["nama"] = admin.nama
        token["no_ktp"] = admin.no_ktp
        token["gh_admin"] = admin.gh_admin
        if admin.gh_admin == False:
            token["id_faskes"] = admin.id_faskes.id_faskes
            token["nama_faskes"] = admin.id_faskes.faskes
        token["jenis_anggota"] = admin.jenis_anggota
        foto = admin.foto_identitas
        if foto:
            token["foto"] = foto.url
        return token
