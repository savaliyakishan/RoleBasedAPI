from django.urls import path

# Views
from user_auth.views import LoginView

app_name = 'user_auth'

urlpatterns = [
    path('login/', LoginView.as_view(), name='LoginView'),
]
