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





# from rest_framework.fields import (  # NOQA # isort:skip
#     BooleanField, CharField, ChoiceField, DateField, DateTimeField, DecimalField,
#     DictField, DurationField, EmailField, Field, FileField, FilePathField, FloatField,
#     HiddenField, HStoreField, IPAddressField, ImageField, IntegerField, JSONField,
#     ListField, ModelField, MultipleChoiceField, ReadOnlyField,
#     RegexField, SerializerMethodField, SlugField, TimeField, URLField, UUIDField,
# )
# from django.db import models
# from rest_framework.relations import (  # NOQA # isort:skip
#     HyperlinkedIdentityField, HyperlinkedRelatedField, ManyRelatedField,
#     PrimaryKeyRelatedField, RelatedField, SlugRelatedField, StringRelatedField,
# )
# from rest_framework.compat import postgres_fields



# class DummyMoviesModelSerializer(serializers.ModelSerializer):
#     serializer_field_mapping = {
#         models.AutoField: IntegerField,
#         models.BigIntegerField: IntegerField,
#         models.BooleanField: BooleanField,
#         models.CharField: CharField,
#         models.CommaSeparatedIntegerField: CharField,
#         models.DateField: DateField,
#         models.DateTimeField: DateTimeField,
#         models.DecimalField: DecimalField,
#         models.DurationField: DurationField,
#         models.EmailField: EmailField,
#         models.Field: ModelField,
#         models.FileField: FileField,
#         models.FloatField: FloatField,
#         models.ImageField: ImageField,
#         models.IntegerField: IntegerField,
#         models.NullBooleanField: BooleanField,
#         models.PositiveIntegerField: IntegerField,
#         models.PositiveSmallIntegerField: IntegerField,
#         models.SlugField: SlugField,
#         models.SmallIntegerField: IntegerField,
#         models.TextField: CharField,
#         models.TimeField: TimeField,
#         models.URLField: URLField,
#         models.UUIDField: UUIDField,
#         models.GenericIPAddressField: IPAddressField,
#         models.FilePathField: FilePathField,
#     }
#     if hasattr(models, 'JSONField'):
#         serializer_field_mapping[models.JSONField] = JSONField
#     if postgres_fields:
#         serializer_field_mapping[postgres_fields.HStoreField] = HStoreField
#         serializer_field_mapping[postgres_fields.ArrayField] = ListField
#         serializer_field_mapping[postgres_fields.JSONField] = JSONField
#     serializer_related_field = PrimaryKeyRelatedField
#     serializer_related_to_field = SlugRelatedField
#     serializer_url_field = HyperlinkedIdentityField
#     serializer_choice_field = ChoiceField

#     class Meta:
#         model = Movies
#         exclude = ["id"]