from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('home', views.index, name='home'),
    path('player/create', views.CreatePlayer.as_view(), name='create_player'),
    path('player/<int:pk>/add_skill', views.add_Skill, name='add_skill'),
    path('player/<int:pk>', views.DetailPlayer.as_view(), name='detail'),
    path('', views.dashboard, name='dashboard'),
    path('teams', views.Teams, name='teams'),
    path('signup', views.SignUp.as_view(), name='signup'),
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
