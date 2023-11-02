from django.urls import path
from . import views

app_name = "potatoapp"

urlpatterns = [
    path("", views.index, name="index"),
    path('home',views.home,name='home'),
    path("previous", views.prev, name="previous"),
    path("next", views.next, name="next"),
    path('accounts/login/',views.loginview,name="login"),
	path('logout',views.logout_view),
	path('accounts/sign_up/',views.sign_up,name="signup"),
	path('reset',views.Resethome,name='reset'), 
	path('passwordreset',views.resetPassword,name="passwordreset"),
    path('artist/<int:pk>',views.artist,name='artist'),
    path('library',views.library,name='library')
]