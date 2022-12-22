from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ask/', views.ask, name="ask"),
    path('login/', views.login, name="login"),
    path('settings/', views.settings, name="settings"),
    path('signup/', views.signup, name="signup"),
    path('tag/<str:tag_name>/', views.tag, name="tag"),
    path('question/<int:pk>/', views.question, name="question"),
    path('hot/', views.hotquestions, name="hot"),
    path('vote/', views.vote, name="vote"),
    path('correct/', views.correct, name="correct"),
    path('logout/', views.logout, name="logout"),
    path('', views.index, name="index")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
