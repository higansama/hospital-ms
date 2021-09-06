from user_management.models import (
    TableBasicUser,
    TableUser,
    TableRekamMedis,
    TableLogPointUser,
    TableUserKeluarga,
)
from rest_framework import serializers
from goldenhour import helpers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableUser
        fields = "__all__"

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


# harusnya udah dipindahin
# class TableRekamMedisApi(serializers.ModelSerializer):
#     class Meta:
#         model = TableRekamMedis
#         fields = "__all__"

#     def create(self, validated_data):

#         no_rekam_medis = helpers.RekamMedisGenerator()
#         print("no_reg_member =>", validated_data["no_reg_member"])
#         validated_data["no_rekam_medis"] = no_rekam_medis
#         inst = TableRekamMedis.objects.create(**validated_data)
#         return inst


class TableLogPointUserApi(serializers.ModelSerializer):
    class Meta:
        model = TableLogPointUser
        fields = "__all__"


class TableKeluargaApi(serializers.ModelSerializer):
    class Meta:
        model = TableUserKeluarga
        fields = "__all__"
