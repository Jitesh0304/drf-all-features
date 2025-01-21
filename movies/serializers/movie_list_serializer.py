from rest_framework import serializers
from ..models import Movies
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings
from rest_framework.utils import html
from django.db import models




class MovieListSerializer(serializers.ListSerializer):

    # def is_valid(self, *, raise_exception=False):
    #     # This implementation is the same as the default,
    #     # except that we use lists, rather than dicts, as the empty case.
    #     assert hasattr(self, 'initial_data'), (
    #         'Cannot call `.is_valid()` as no `data=` keyword argument was '
    #         'passed when instantiating the serializer instance.'
    #     )
    #     if not hasattr(self, '_validated_data'):
    #         try:
    #             self._validated_data = self.run_validation(self.initial_data)
    #         except ValidationError as exc:
    #             self._validated_data = []
    #             self._errors = exc.detail
    #         else:
    #             self._errors = []
    #     if self._errors and raise_exception:
    #         raise ValidationError(self.errors)
    #     return not bool(self._errors)



    # def is_valid(self, *, raise_exception=False):
    #     """
    #     Override is_valid to handle validation for a list of items explicitly.
    #     """
    #     self._validated_data = []
    #     self._errors = []
    #     # Validate each item in the list
    #     for idx, item in enumerate(self.initial_data):
    #         serializer = self.child.__class__(data=item, context=self.context)
    #         if serializer.is_valid():
    #             self._validated_data.append(serializer.validated_data)
    #         else:
    #             self._errors.append({idx: serializer.errors})
    #     if self._errors and raise_exception:
    #         raise serializers.ValidationError(self._errors)
    #     # Return whether the data is valid or not
    #     return not bool(self._errors)



    def is_valid(self, *, raise_exception=False):
        assert hasattr(self, 'initial_data'), (
            'Cannot call `.is_valid()` as no `data=` keyword argument was '
            'passed when instantiating the serializer instance.'
        )
        """
        Override is_valid to handle validation for a list of items explicitly.
        """
        if not isinstance(self.initial_data, list):
            raise ValidationError("Expected a list of items but got type `{}`.".format(type(self.initial_data).__name__))

        self._validated_data = []
        self._errors = []

        for index, item in enumerate(self.initial_data):
            # print(item)
            try:
                validated_item = self.run_validation([item])
                # print('ok')
                self._validated_data.append(validated_item)
                # print('ok2')
            except ValidationError as exc:
                self._errors.append({index: exc.detail})

        if self._errors and raise_exception:
            raise ValidationError(self._errors)

        return not bool(self._errors)
    
        # self._validated_data = []
        # self._errors = []
        # print(self.initial_data)
        # if not hasattr(self, '_validated_data'):
        #     for index, item in enumerate(self.initial_data):
        #         try:
        #             self._validated_data = self.run_validation(self.initial_data)
        #         except ValidationError as exc:
        #             self._validated_data = []
        #             self._errors = exc.detail
        #         else:
        #             self._errors = []
        #     if self._errors and raise_exception:
        #         raise ValidationError(self._errors)
        # return not bool(self._errors)


    def validate(self, data):
        # print('in validate 2')
        if not data:
            raise serializers.ValidationError("At least one movie must be provided.")

        # Validate against existing instances (if provided)
        if self.instance:
            existing_ids = {movie.id for movie in self.instance}
            for item in data:
                movie_id = item.get("id")
                if movie_id and movie_id not in existing_ids:
                    raise serializers.ValidationError(
                        f"Movie with ID {movie_id} does not exist in the current dataset."
                    )
        return data

    # ## will not work in post method
    # def create(self, validated_data):
    #     ## Create a list of Product instances
    #     product_data = [Movies(**item) for item in validated_data]
    #     return Movies.objects.bulk_create(product_data)

    def create(self, validated_data):
        return super().create(validated_data)

    # def update(self, instance, validated_data):
    #     # print(instance)
    #     # return super().update(instance, validated_data)
    #     return_list = []
    #     for index, item in enumerate(instance):
    #         # self.child.update(item, validated_data[index])
    #         return_dt = super().update(item, validated_data[index])
    #         return_list.append(return_dt)
    #     return return_list


    # def update(self, instance, validated_data):
    #     instance_dict = {movie.id: movie for movie in instance}
    #     updated_instances = []
    #     for item in validated_data:
    #         movie_id = item.get("id")
    #         movie_instance = instance_dict.get(movie_id)
    #         if movie_instance:
    #             # print(movie_instance)
    #             for attr, value in item.items():
    #                 # Only set attributes that are concrete fields
    #                 if attr in ['title', 'production', 'industry', #'actors', 
    #                             'director', 'producer', 'bugget', 'total_collection', 'release_date']:
    #                     setattr(movie_instance, attr, value)
    #             updated_instances.append(movie_instance)
    #     # Bulk update with only concrete fields
    #     return Movies.objects.bulk_update(
    #         updated_instances,
    #         ['title', 'production', 'industry',# 'actors', 
    #         'director', 'producer', 'bugget', 'total_collection', 'release_date']
    #     )
    def update(self, instance, validated_data):
        list_of_instances = []
        for i, (inst, val_data) in enumerate(zip(instance, validated_data)):
            # print(i)
            # print(inst)
            # print(val_data)
            inst.title = val_data.get('title', inst.title)
            inst.production = val_data.get('production', inst.production)
            inst.industry = val_data.get('industry', inst.industry)
            if val_data.get('actors'):
                inst.actors.set(val_data.get('actors'))
            inst.director = val_data.get('director', inst.director)
            inst.producer = val_data.get('producer', inst.producer)
            inst.bugget = val_data.get('bugget', inst.bugget)
            inst.total_collection = val_data.get('total_collection', inst.total_collection)
            inst.release_date = val_data.get('release_date', inst.release_date)
            inst.save()
            list_of_instances.append(inst)
        return list_of_instances


    
        # instance_dict = {movie.id: movie for movie in instance}
        # updated_instances = []
        # for item in validated_data:
        #     movie_id = item.get("id")
        #     movie_instance = instance_dict.get(movie_id)

        #     if movie_instance:
        #         # print(movie_instance)
        #         for attr, value in item.items():
        #             # Only set attributes that are concrete fields
        #             if attr in ['title', 'production', 'industry', #'actors', 
        #                         'director', 'producer', 'bugget', 'total_collection', 'release_date']:
        #                 setattr(movie_instance, attr, value)
        #         updated_instances.append(movie_instance)
        # # Bulk update with only concrete fields
        # return Movies.objects.bulk_update(
        #     updated_instances,
        #     ['title', 'production', 'industry',# 'actors', 
        #     'director', 'producer', 'bugget', 'total_collection', 'release_date']
        # )


    def to_internal_value(self, data):
        """
        List of dicts of native values <- List of dicts of primitive datatypes.
        """
        if html.is_html_input(data):
            data = html.parse_html_list(data, default=[])

        if not isinstance(data, list):
            message = self.error_messages['not_a_list'].format(
                input_type=type(data).__name__
            )
            raise ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: [message]
            }, code='not_a_list')

        if not self.allow_empty and len(data) == 0:
            message = self.error_messages['empty']
            raise ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: [message]
            }, code='empty')

        if self.max_length is not None and len(data) > self.max_length:
            message = self.error_messages['max_length'].format(max_length=self.max_length)
            raise ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: [message]
            }, code='max_length')

        if self.min_length is not None and len(data) < self.min_length:
            message = self.error_messages['min_length'].format(min_length=self.min_length)
            raise ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: [message]
            }, code='min_length')

        # ret = []
        # errors = []
        # for item in data:
        #     try:
        #         validated = self.child.run_validation(item)
        #     except ValidationError as exc:
        #         errors.append(exc.detail)
        #     else:
        #         ret.append(validated)
        #         errors.append({})
        # if any(errors):
        #     raise ValidationError(errors)
        # return ret

        ret = []
        errors = []

        for item in data:
            # print(item)
            try:
                if not item.get('id'):
                    validated = self.child.run_validation(item)
                else:
                    self.child.instance = self.instance.get(id=item['id'])
                    self.child.initial_data = item
                    # Until here
                    validated = self.child.run_validation(item)
            except ValidationError as exc:
                errors.append(exc.detail)
            else:
                ret.append(validated)
                errors.append({})

        if any(errors):
            raise ValidationError(errors)
        return ret



    def save(self, **kwargs):
        """
        Save and return a list of object instances.
        """
        # Guard against incorrect use of `serializer.save(commit=False)`
        assert 'commit' not in kwargs, (
            "'commit' is not a valid keyword argument to the 'save()' method. "
            "If you need to access data before committing to the database then "
            "inspect 'serializer.validated_data' instead. "
            "You can also pass additional keyword arguments to 'save()' if you "
            "need to set extra attributes on the saved model instance. "
            "For example: 'serializer.save(owner=request.user)'.'"
        )
        
        validated_data = []
        for attrs in self.validated_data:
            if isinstance(attrs, list):
                for attr in attrs:
                    validated_data.append({**attr, **kwargs})
            else:
                validated_data.append({**attrs, **kwargs})

        # validated_data = [
        #     {**attrs, **kwargs} for i,attrs in enumerate(self.validated_data)
        # ]

        if self.instance is not None:
            self.instance = self.update(self.instance, validated_data)
            assert self.instance is not None, (
                '`update()` did not return an object instance.'
            )
        else:
            self.instance = self.create(validated_data)
            assert self.instance is not None, (
                '`create()` did not return an object instance.'
            )

        return self.instance


    def to_representation(self, data):
        # print(data)
        """
        List of object instances -> List of dicts of primitive datatypes.
        """
        # Dealing with nested relationships, data can be a Manager,
        # so, first get a queryset from the Manager if needed
        iterable = data.all() if isinstance(data, models.Manager) else data

        return [
            self.child.to_representation(item) for item in iterable
        ]


class MovieSerializer_list(serializers.ModelSerializer):

    class Meta:
        model = Movies
        fields = ['id', 'title', 'production', 'industry', 'actors', 'director', 'producer', 'bugget', 'total_collection',
                  'release_date']
        # extra_kwargs = {
        #     'actors': {'required': True},
        # }
        list_serializer_class = MovieListSerializer


    # def validate(self, attrs):
    #     print('in validate 1')
    #     return super().validate(attrs)


