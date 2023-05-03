from django.urls import path
from . import views

urlpatterns = [
    path('', views.landingpage, name="landingpage"),
    path('landingpage/', views.landingpage, name="landingpage"),
    path('signup/', views.signup, name="signup"),
    path('signin/',views.signin, name="signin"),
    path('forget_pass/',views.forget_pass, name="forget_pass"),
    # path("home/",views.home,name="home"),
    path('reset_password/',views.reset_password, name='reset_password'),
    path('reset_code/',views.reset_code, name='reset_code'),
    path('reset_passwordDone/',views.reset_passwordDone, name='reset_passwordDone'),
    path('send_offerEmail/',views.send_offerEmail, name='send_offerEmail'),
    path('joinclass/',views.joinclass, name='joinclass'),
]
