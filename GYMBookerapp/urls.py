from django.urls import path
from . import views

urlpatterns = [
    path('', views.landingpage, name="landingpage"),
    path('landingpage/', views.landingpage, name="landingpage"),
    path('signup/', views.signup, name="signup"),
    path('signin/',views.signin, name="signin"),
    # path("home/",views.home,name="home"),
]
