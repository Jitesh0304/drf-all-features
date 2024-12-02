from rest_framework import serializers
from ..models import Movies



class MoviesModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movies
        fields ="__all__"
        # excludes = ["field_1"]
        # depth = 2


    # def update(self, instance, validated_data):
    #     instance.bugget = validated_data.get('bugget', instance.bugget)
    #     instance.save()
    #     return instance



class DummyMoviesModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movies
        exclude = ["id"]
        # depth = 2
