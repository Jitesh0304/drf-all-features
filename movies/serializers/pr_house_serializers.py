from rest_framework import serializers
from ..models import ProductionHouse
from account.serializers import UserModelSeralizer, UserSimpleSeralizer
from django.db import transaction, DatabaseError
from account.models import User



class ProductionHouseModelSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model = ProductionHouse
        fields ="__all__"
        # excludes = ["field_1"]


    def update(self, instance, validated_data):
        
        return super().update(instance, validated_data)



class DummyProductionHouseModelSerializer(serializers.ModelSerializer):
    owner = UserSimpleSeralizer()
    # owner = UserModelSeralizer()      ## details of user data
    # partners = UserModelSeralizer(many=True)    ## use for retrieve only, (note:- not for create/update)
            ## OR
    # owner = serializers.PrimaryKeyRelatedField(read_only=True)        ## only pk value
    # partners = serializers.PrimaryKeyRelatedField(many = True,read_only=True)

    # owner = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model = ProductionHouse
        fields = "__all__"
        # exclude = ["id"]
        # read_only_fields = ['field_1','field_2']
        # extra_kwargs = {'pr_name': {'write_only': True}}      ## write_only true will helpfull during creating / updating

    def validate(self, attrs):
        # print(attrs['owner'])
        return super().validate(attrs)
    
    # def validate_owner(self, value):
    #     email = value.get('email')
    #     if email:
    #         if User.objects.filter(email=email).exists():
    #             raise serializers.ValidationError("User with this email already exists")
    #     return value
    

    def create(self, validated_data):
        try:
            with transaction.atomic():
                owner_dt = validated_data.pop('owner')
                owner_dt['password'] = 'random_password'
                # usr = UserModelSeralizer.create(UserModelSeralizer(), validated_data=owner_dt)
                    ## OR
                # user_serializer = UserModelSeralizer(data=owner_dt)
                # user_serializer.is_valid(raise_exception=True)
                # usr = user_serializer.save()
                    ## OR
                usr = User.objects.get_or_create(**owner_dt)[0]
                all_partners = validated_data.pop('partners')
                pr_house = ProductionHouse.objects.create(owner=usr, **validated_data)
                pr_house.partners.set(all_partners)
                return pr_house
        except DatabaseError:
            raise serializers.ValidationError("Database Error")
        except Exception as e:
            raise serializers.ValidationError(e)


    def save(self, **kwargs):
        return super().save(**kwargs)
    
    def update(self, instance, validated_data):
        instance.pr_name = validated_data.get('pr_name', instance.pr_name)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.industry = validated_data.get('industry', instance.industry)
        if validated_data.get('partners'):
            instance.partners.set(validated_data.get('partners'))
        if validated_data.get('owner'):
            del validated_data['owner']['date_of_birth']
            usr = User.objects.get(**validated_data.get('owner'))
            instance.owner = usr
            # instance.owner = validated_data.get('owner', instance.owner)
        instance.save()
        return instance
    

    def to_representation(self, instance):
        """
        Outgoing (serialization)

        This method is used to convert the internal representation of an object (typically a Django model instance) into a 
        serialized format suitable for rendering, such as JSON. It is called when the serializer is preparing to send data out 
        (e.g., in response to a client request).
        """
        representation = super().to_representation(instance)
        representation['pr_name'] = representation['pr_name'].upper()
        return representation


    def to_internal_value(self, data):
        """
        Incoming (deserialization)

        This method is responsible for converting the incoming serialized data (e.g., from a JSON request) back into an internal 
        representation that can be validated and saved in the database. It is called when deserializing data.

        When data is received from a client (for example, in a POST request), DRF needs to convert this serialized data 
        (often in JSON format) into a format that can be processed internally, typically into Python objects.

        The to_internal_value method is called as part of the deserialization process. This method takes the incoming data and 
        transforms it into an internal representation that the serializer can work with.

        Incoming data → to_internal_value → Internal representation → Validation → (if valid) Save or further processing.
        """
        pr_name = data.pop('pr_name', None)
        if pr_name:
            data['pr_name'] = pr_name.upper()
        return super().to_internal_value(data)

