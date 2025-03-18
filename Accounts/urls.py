from django.urls import path
from .views import RegisterView,LoginView,UpdateProfile,TokenVerification,ResetPassword,ChangePassword,GetProfile,WebLogout,WebLogin,ProfileView
urlpatterns = [
    path('Register',RegisterView.as_view(),name='register'),
    path('Login',LoginView.as_view(),name='login'),
    path('TokenVerification',TokenVerification,name='token_verification'),
    path('reset_password',ChangePassword.as_view()),
    path('update_profile',UpdateProfile,name='update_profile'),
    path('profile',ProfileView.as_view()),
    path('getProfile',GetProfile,name='get_profile'),
    path('logout',WebLogout,name='weblogout'),
    path('login',WebLogin.as_view(),name='weblogin'),
    # pathc('res')
    
]
