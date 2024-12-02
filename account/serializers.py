from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer , TokenBlacklistSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
import os


    ## custom token generator
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
        ## send the user data to get the token
    def get_token(cls, user):
            ## check the user is verify or not
        if user is not None:
                ## generate token for the user.. it will give you refresh and access token
            token = super().get_token(user)
                # Add username and email to the token payload
                ## add extra field in the payload
            token['name'] = user.name
            token['email'] = user.email
            return token
        else:
            raise serializers.ValidationError('You are not verified')
    # def validate(self, attrs):
    #     data = super().validate(attrs)
    #           # Add username and email to the response data
    #     data['name'] = self.user.name
    #     data['email'] = self.user.email
    #     data['organization'] = self.user.organization
    #     return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        ## call super() to get the access token and refresh token
        data = super().validate(attrs)
        ## validate the input data ( attrs )
        ## take the refresh token from the attrs
        refresh_token = RefreshToken(attrs['refresh'])
        ## take the user email from the refresh token
        email = refresh_token.payload.get('email')
        try:
            ## take the user details from the database
            user = User.objects.get(email = email)
            ## decode the generated jwt token
            decodeJTW = jwt.decode(str(data['access']), os.getenv('DJANGO_SECRET_KEY'), algorithms=["HS256"])
                # add payload here
            decodeJTW['name'] = str(user.name)
            decodeJTW['email'] = str(user.email)
            ## encode the modified jwt token
            encoded = jwt.encode(decodeJTW, os.getenv('DJANGO_SECRET_KEY'), algorithm="HS256")
            ## replace the access token with the modified one
            data['access'] = encoded
            user.save()
            ## return the newly generated token
            return data
        except:
            return data
        

        ## user registration 
class UserRegistrationSerializer(serializers.ModelSerializer):
        ## password field is write only
    password2 = serializers.CharField(required=True,style = {'input_type':'password'}, write_only =True)
    class Meta:
        model = User
        fields = ['email','name', 'date_of_birth','password','password2']          ## mension the required fileds (( otp  ))
        extra_kwargs = {
            'password':{'write_only':True},            ## password => write_only field
        }

            ## validate both passwords are same or not
    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')

        if password != password2:
            raise serializers.ValidationError('Password and Confirm password does not match.....')
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long....")
        return data

                ## if the validation is successfull then create that user
    def create(self, validate_data):
        del validate_data['password2']
        return User.objects.create_user(**validate_data)



                ## This is for login page
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        model = User
        fields = ['email','password']               ## this two fields we need during login




            ## this is for perticular user profile 
class UserProfileSeralizer(serializers.ModelSerializer):
    # date_of_birth = serializers.DateTimeField(format="%d/%m/%Y")
    class Meta:
        model = User
        fields = ['email','name','date_of_birth','is_active','is_admin']
    
    def to_representation(self, instance):
        user = self.context.get('user')
        data = super().to_representation(instance)
        if not user.is_admin:
            data.pop("is_admin")
        return data


            ## this is for perticular user profile 
class UserModelSeralizer(serializers.ModelSerializer):
    # date_of_birth = serializers.DateTimeField(format="%d/%m/%Y")
    class Meta:
        model = User
        exclude = ["password"]
    
    def to_representation(self, instance):
        # print(instance.is_admin)
        data = super().to_representation(instance)
        # print(data)
        if not data['is_admin']:
            data.pop("is_admin")
        return data


            ## this is for password change
class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length= 255, style= {'input_type':'password'}, write_only =True)
    password2 = serializers.CharField(max_length= 255, style= {'input_type':'password'}, write_only =True)
    class Meta:
        fields = ['password','password2']

        ## validate both passwords are same or not
    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
            ## take the user data from context send from views class
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError('Password and Confirm password does not match')
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long....")
            ## set the new password in user account
        user.set_password(password)
        user.save()
        return data
    

class CustomTokenBlacklistSerializer(TokenBlacklistSerializer):
    def validate(self, attrs):
        # print(attrs)
        refresh = attrs.get("refresh")
        token = RefreshToken(refresh).blacklist()
        return "success"