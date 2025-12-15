from django.contrib import admin
from django.urls import path
from chatbot import views
from django.conf.urls.static import static

from chatbruti import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ask/', views.ask_patoche, name='ask'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)