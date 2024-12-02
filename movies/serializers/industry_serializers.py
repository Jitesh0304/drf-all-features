from rest_framework import serializers
from rest_framework.serializers import UniqueTogetherValidator
from ..models import MovieIndustry



class MovieIndustryModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovieIndustry
        fields ="__all__"
        # excludes = ["field_1"]
    
    # def create(self, validated_data):
    #     return MovieIndustry.objects.create(**validated_data)

    # def save(self, **kwargs):
    #     return super().save(**kwargs)

    # def validate(self, attrs):
    #     if "language" not in attrs:
    #         raise serializers.ValidationError("Language is missing")
    #     return super().validate(attrs)

    # # field level validation
    # def validate_language(self, value):
    #     """
    #     Check that the blog post is about Django.
    #     """
    #     if len(value) < 2:
    #         raise serializers.ValidationError("Language must have at leasst 2 characters.")
    #     return value



def language_length(value):
    if len(value) < 2:
        raise serializers.ValidationError('Language must have at leasst 2 characters.')

class DummyMovieIndustryModelSerializer(serializers.Serializer):
    language = serializers.CharField(max_length=20, validators = [language_length])             ## serializers.IntegerField(choices=[101, 102, 103, 201])
    industry_name = serializers.CharField(max_length=30)
    country = serializers.CharField(max_length=30)

    # country = serializers.CharField(read_only=True, default=...)

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=MovieIndustry.objects.all(),
                fields=['country', 'language']
            )
        ]

    def create(self, validated_data):
        return MovieIndustry.objects.create(**validated_data)

    # def save(self, **kwargs):
    #     return super().save(**kwargs)