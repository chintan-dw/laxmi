from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('cdr/', views.cdrView, name='cdr'),
    path('convert/', views.convert, name='convert'),
    path('usingv1/',views.apiv1, name='usingv1')
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)