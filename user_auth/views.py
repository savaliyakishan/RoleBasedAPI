# drf
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

# django
from django.contrib.auth import authenticate

# base
from base.base_helper import GlobalHelperFunction


# Create your views here.
class LoginView(APIView, GlobalHelperFunction):
    """
    APIView for user login that authenticates credentials and generates a JWT token.
    Validates presence of username and password, then uses Django's authentication system to verify credentials.
    Returns a JWT access token if authentication is successful, with appropriate error messages otherwise.
    """

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # validation
        self.value_list = {"Username": username, "Password":password}
        self.validations()
        if self.Response:
            return Response({"success": False, 'message': f"{self.key} is required."}, status=status.HTTP_400_BAD_REQUEST)

        # check user authentication
        user = authenticate(username=username, password=password)

        if not user:
            return Response({"success": False, 'message': "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        
        # generate token
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "success": True,
            'access_token': str(refresh.access_token),
            'token_type': 'bearer'
        }, status=status.HTTP_200_OK)