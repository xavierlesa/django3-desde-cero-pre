from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from portfolio import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.project_list, name='project_list'),
    path('<slug:slug>', views.project_detail, name='project_detail'),
    path('tag/<slug:tag>', views.project_filter_list, name='project_filter_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
