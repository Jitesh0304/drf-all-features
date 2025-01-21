from django.urls import path, include
from account.views import CustomTokenObtainPairView, CustomTokenRefreshView, UserRegistrationView, UserLoginView,\
    UserProfileView, UserChangePasswordView, LogoutView, DeleteBlacklistAdOutstandingView, RetrievAllUsersProfileView, \
    RetrievUsersProfileViewByID
   ##  ResetPasswordView, ActivationConfirm, ForgotPasswordEmailSendView, ForgotPasswordEmailVerifyView,
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    # path('gettoken/',TokenObtainPairView.as_view(), name= 'token_pair'),
    # path('refreshtoken/', TokenRefreshView.as_view(), name= 'token_resfresh'),
    path('gettoken/',CustomTokenObtainPairView.as_view(), name= 'token-pair'),
    path('refreshtoken/', CustomTokenRefreshView.as_view(), name= 'token-resfresh'),
    path('verifytoken/',TokenVerifyView.as_view(), name= 'token-verify'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name= 'login'),
    path('profile/', UserProfileView.as_view(), name= 'profile'),
    path('all-user-profile/', RetrievAllUsersProfileView.as_view(), name= 'profile-list'),
    path('change-password/', UserChangePasswordView.as_view(), name= 'changepassword'),
    path('logout/', LogoutView.as_view(), name= 'logout'),
    path('deletetoken/', DeleteBlacklistAdOutstandingView.as_view(), name= 'deletetoken'),
    path('profile/<int:id>/', RetrievUsersProfileViewByID.as_view(), name= 'user-detail'),
    
]