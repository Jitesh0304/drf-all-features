from rest_framework import serializers
from ..models import ProductionHouse
from account.serializers import UserModelSeralizer


class ProductionHouseModelSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model = ProductionHouse
        fields ="__all__"
        # excludes = ["field_1"]


    def update(self, instance, validated_data):
        
        return super().update(instance, validated_data)
    



class DummyProductionHouseModelSerializer(serializers.ModelSerializer):
    # owner = UserModelSeralizer()
    # partners = UserModelSeralizer(many=True)
            ## OR
    # owner = serializers.PrimaryKeyRelatedField(read_only=True)
    # partners = serializers.PrimaryKeyRelatedField(many = True,read_only=True)

    owner = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model = ProductionHouse
        exclude = ["id"]
        # read_only_fields = ['field_1','field_2']

    def validate(self, attrs):
        print(attrs['owner'])
        return super().validate(attrs)


