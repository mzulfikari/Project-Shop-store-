from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path ,include
from Shop import settings

urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('Home.urls')),
        path('', include('account.urls')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)