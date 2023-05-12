from django.urls import path
from . import views
from .models import *

app_name = 'neword'

urlpatterns = [ 
	path('',views.Home, name='home'),
	path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('text_trans/', views.text_trans, name='text_trans'),
    path('upload/', views.upload_file, name='file_trans'),
    path('delete_word/<int:word_id>/', views.delete_word, name='delete_word'),
    path('edit_word/<int:pk>/', views.edit_word, name='edit_word'),
    path('get_data/', views.get_data, name='get_data'),
]