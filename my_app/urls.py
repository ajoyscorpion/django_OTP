from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name="home"),
    path("login",views.register,name="register"),
    path("signIn",views.signInOrVerifyOTP,name="signInOrVerifyOTP"),
    path('logout',views.logout_view,name="logout"),
    #path('verifyOTP',views.verify_otp,name="signInOrVerifyOTP")
]