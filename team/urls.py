from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', views.index, name='index'),
    path('player/create', views.CreatePlayer.as_view(), name='create_player'),
    path('player/<int:pk>/add_skill', views.add_Skill, name='add_skill'),
    path('player/<int:pk>', views.DetailPlayer.as_view(), name='detail'),
    path('', views.dashboard, name='dashboard'),
    # path('teams', views.Teams, name='teams'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
