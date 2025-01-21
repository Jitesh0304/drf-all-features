from rest_framework import serializers
from ..models import ProductionHouse, MovieIndustry
from django.db import transaction, DatabaseError
from account.models import User



# class ProductionHouseHypelinkedSerializer(serializers.HyperlinkedModelSerializer):
#     """
#     lookup_field is a Django Rest Framework (DRF) attribute used to specify the model field that should be used to uniquely 
#     identify an object when constructing or resolving URLs for API endpoints. By default, DRF uses the pk (primary key) field 
#     of a model as the identifier.
#     """
#     owner = serializers.HyperlinkedRelatedField(
#         view_name='user-detail',  # Assuming you have a URL conf for User detail
#         lookup_field='id',
#         queryset=User.objects.all()
#     )
#     partners = serializers.HyperlinkedRelatedField(
#         lookup_field='id',
#         many=True,
#         view_name='user-detail',  # Assuming you have a URL conf for User detail
#         queryset=User.objects.all()
#     )
#     industry = serializers.HyperlinkedRelatedField(
#         view_name='movieindustry-detail',  # Assuming you have a URL conf for MovieIndustry detail
#         queryset=MovieIndustry.objects.all(),
#         lookup_field='pk'
#     )
#     class Meta:
#         model = ProductionHouse
#         fields = ['url', 'pr_name', 'owner', 'partners', 'industry', 'start_date']  # Include 'url' for hyperlinking
#         # extra_kwargs = {'url': {'lookup_field': 'id'}}


                  ## OR ##

class ProductionHouseHypelinkedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductionHouse
        fields = ['url', 'pr_name', 'owner', 'partners', 'industry', 'start_date']  # Include 'url' for hyperlinking
        extra_kwargs = {
            'url': {'view_name': 'productionhouse-detail', 'lookup_field': 'pk'},
            'owner': {'view_name': 'user-detail', 'lookup_field': 'id'},
            'partners': {'view_name': 'user-detail', 'lookup_field': 'id'},
            'industry': {'view_name': 'movieindustry-detail', 'lookup_field': 'pk'},
        }



