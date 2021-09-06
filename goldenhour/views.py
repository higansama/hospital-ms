from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from .jwtclaim import MyTokenObtainPairSerializer, DokterJWTSerializer
from django.contrib.auth import authenticate, logout
from django.http import HttpResponseRedirect, HttpResponse, request
import requests
from django.shortcuts import redirect, render

class LoginUserTokenGenerator(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class LoginDokterTokenGenerator(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = DokterJWTSerializer


def AuthSession(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            authenticate(request ,username=username, password=password)
            return HttpResponseRedirect('/cabinet',None, None)
        except Exception:
            return HttpResponseRedirect('/',{'error': str(Exception)})

@login_required
def logoutAll(request):
    logout(request)
    return HttpResponseRedirect("/pasien/login")