from django.urls import path, include
from django.contrib import admin

# base
from base.custom_exception import custom404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include([
        path('auth/', include('user_auth.urls', namespace='user_auth')),
        path('users/', include('user_management.urls', namespace='user_management')),
        path('entries/', include('entry_management.urls', namespace='entry_management')),
    ])),
]   

handler404 = custom404