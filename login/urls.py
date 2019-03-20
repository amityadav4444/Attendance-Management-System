from django.urls import path
from login import views
from django.contrib.auth import views as auth_views
from login.forms import CustomAuthForm

urlpatterns = [
	path('', auth_views.login, name='login', kwargs={"authentication_form":CustomAuthForm}),
	path('home/', views.home, name='home'),
    path('logout/', auth_views.logout, name='logout'),
	path('mark-attendance/<str:stri>/<str:st>/', views.markAttendance, name='markAttendance'),
	path('add/<str:stri>/<str:st>/', views.add, name='add'),
	path('analyze/<str:stri>/', views.analyze, name='analyze'),
	path('update/', views.update, name='update'),
	path('ChangePassword/', views.ChangePassword, name='ChangePassword'),
	path('CP/', views.CP, name='CP'),
]   