from rest_framework import serializers
from user_management.models import TablePoli, TableFaskes, TableDivisi



class FaskesApi(serializers.ModelSerializer):
   class Meta:
      model = TableFaskes
      fields = "__all__"


class DivisiApi(serializers.ModelSerializer):
   class Meta:
      model = TableDivisi
      fields = "__all__"
   

class PoliApi(serializers.ModelSerializer):
   class Meta:
      model = TablePoli
      fields = "__all__"