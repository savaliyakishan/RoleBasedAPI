from django.urls import path

# views
from user_management.views import CreateUserView, UpdateDeleteUserView

app_name = 'user_management'

urlpatterns = [
    path('', CreateUserView.as_view(), name='CreateUserView'),
    path('<int:pk>', UpdateDeleteUserView.as_view(), name='UpdateDeleteUserView'),
]
