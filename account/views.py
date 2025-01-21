from django.shortcuts import render
from .serializers import CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer, UserRegistrationSerializer, \
    UserChangePasswordSerializer, UserLoginSerializer, UserProfileSeralizer, CustomTokenBlacklistSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from datetime import datetime
from rest_framework.views import APIView
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from datetime import timedelta
from rest_framework import generics
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .custom_auth import CustomAuthentication
from .custom_permission import NameCharPermission





        ## generate token for user
# def get_tokens_for_user(user):
        ## send the user details to RefreshToken.for_user() .. and get the access token and refresh token
#     refreshToken = RefreshToken.for_user(user)
#     accessToken = refreshToken.access_token
#             ## decode the JWT .... mension the same name of th e secrete_key what ever you have written in .env file
#     decodeJTW = jwt.decode(str(accessToken), config('DJANGO_SECRET_KEY'), algorithms=["HS256"])
#             # add payload here!!
#     decodeJTW['user'] = str(user)
#     decodeJTW['name'] = str(user.name)
#             # encode
#     encoded = jwt.encode(decodeJTW, config('DJANGO_SECRET_KEY'), algorithm="HS256")
#     return {
#         'refresh': str(refreshToken),
#         'access': str(encoded),
#     }


# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer
            ####### OR ######


    ## generate new token during login time
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
        ## send user data by a post request
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.user
            
            user = User.objects.get(email = user)
                ## take the token from the serializer
            token = serializer.validated_data
                ## create refresh_token
            refresh_token = RefreshToken.for_user(user)
                ## add user details if required
            response_data = {
                'access': str(token['access']),
                'refresh': str(refresh_token),
                # 'is_admin': user.is_admin,
            }
            user.last_login = timezone.now()
            user.save()
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'msg': f'Error in generating token. {e}'}, status=status.HTTP_400_BAD_REQUEST)


        ## regenerate the access token using refresh token
class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer
    def post(self, request, *args, **kwargs):               ## use this or not .. you will get result
        data = super().post(request, *args, **kwargs)
        return data
    

    # create new user 
class UserRegistrationView(APIView):
        ## render the error message using custome render class
    # renderer_classes = [UserRenderer]
    def post(self, request, format =None):
        try:
            # host_name = request.META.get('HTTP_HOST', None)
            # print(host_name)
            serializer = UserRegistrationSerializer(data = request.data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                return Response({'msg': 'Registration Successful'}, status.HTTP_201_CREATED)
            return Response({'msg': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)



        ## This is for User login
class UserLoginView(APIView):
    ## render the error message using custome render class
    # renderer_classes = [UserRenderer]
    def post(self, request, format= None):
        try:
            serializer = UserLoginSerializer(data= request.data)
            if serializer.is_valid():        ## raise_exception= True

                email = serializer.data.get('email')
                password = serializer.data.get('password')
                
                user_auth = authenticate(email= email, password = password)
                if user_auth is not None:
                    user = User.objects.get(email= email)
                        ## generate the token using serializer class
                    access = CustomTokenObtainPairSerializer.get_token(user)
                        ## generate the refresh token
                    refresh = RefreshToken.for_user(user)
                    token = {
                        'access':str(access.access_token),
                        'refresh':str(refresh),
                        'is_admin': user.is_admin,
                        }
                        ## generate the token using view class
                    # token_obtain_pair_view = CustomTokenObtainPairView()
                    # token_response = token_obtain_pair_view.post(request)
                    user.last_login = timezone.now()
                    user.save()
                    return Response({'token': token}, status=status.HTTP_200_OK)
                else:
                    return Response({'msg':'Email or Password is not Valid'},status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'msg':serializer.errors}, status= status.HTTP_400_BAD_REQUEST)    
        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format= None):
        try:
            user = request.user
            serializer = UserProfileSeralizer(user, context={"user":user})
            return Response(serializer.data, status= status.HTTP_200_OK)
        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class RetrievAllUsersProfileView(APIView):

    # authentication_classes = [CustomAuthentication, SessionAuthentication, BasicAuthentication]

    permission_classes = [IsAuthenticated|IsAdminUser]
    # permission_classes = [IsAdminUser, NameCharPermission]

    def get(self, request, format= None):
        # print(self.get_permissions())
        try:
            # print(request.content_type)
            # print(request.META.get('HTTP_CONTENT_TYPE'))
            # print(request.query_params)
            users = User.objects.all()
            serializer = UserProfileSeralizer(users, context={"user": request.user}, many=True)
            return Response(serializer.data, status= status.HTTP_200_OK)
        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class RetrievUsersProfileViewByID(APIView):

    def get(self, request, id, format= None):
        try:
            user = User.objects.get(id = id)
            serializer = UserProfileSeralizer(user, context={"user": request.user})
            return Response(serializer.data, status= status.HTTP_200_OK)
        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class UserChangePasswordView(APIView):
    # renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format= None):
        try:
            serializer = UserChangePasswordSerializer(data = request.data, context ={'user':request.user})
            if serializer.is_valid(raise_exception= True):         
                return Response({'msg':'Password Changed Successfully'}, status.HTTP_200_OK)
            return Response({'msg':serializer.errors}, status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            serializer = CustomTokenBlacklistSerializer(data= request.data)
            if serializer.is_valid():
                # print(serializer.validated_data)
                # token = RefreshToken(serializer.validated_data['refresh'])
                # token.blacklist()
                return Response({'msg':"Logout successful"}, status= status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'msg':str(e)}, status= status.HTTP_400_BAD_REQUEST)



    ## logout without serializer
# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, format=None):
#         try:
#             if "refresh" in request.data:
#                 token = RefreshToken(request.data.get("refresh"))
#                 token.blacklist()
#                 return Response({'msg':"Logout successful"}, status= status.HTTP_200_OK)
#             else:
#                 return Response({'msg':"Refrest token required ..."}, status= status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({'msg':str(e)}, status= status.HTTP_400_BAD_REQUEST)



class DeleteBlacklistAdOutstandingView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        try:
            user = request.user
            outstanding , _ = OutstandingToken.objects.filter(expires_at__lte = timezone.now()).delete()
                ## token  == > is the field name ......   created_at is the outstanding model field name which is a OneToOne field with token
            blacklist, _ = BlacklistedToken.objects.filter(token__created_at__lte= timezone.now()- timedelta(minutes=10)).delete()
            return Response({'msg':f'Deleted {outstanding} outstanding tokens and {blacklist} blacklisted tokens.'}, status= status.HTTP_200_OK)
            # return Response({'msg':"Deleted ....."}, status= status.HTTP_200_OK)
        except Exception as e:
            return Response({'msg':str(e)}, status= status.HTTP_400_BAD_REQUEST)
        


