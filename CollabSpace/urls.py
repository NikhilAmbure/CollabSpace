from django.contrib import admin
from django.urls import path, include
from users.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('verify-otp/', OTPVerifyAPI.as_view(), name='verify-otp'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('api/', include('tasks.urls')),
    path('api/', include('_docs.urls')),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)