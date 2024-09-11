# drf
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

# serializer
from user_management.serializers import UserSerializer

# model
from user_management.models import User


# Create your views here.
class CreateUserView(APIView):
    """
    APIView for creating and listing User objects.
    POST creates a new user with the provided data, while GET retrieves all users ordered by ID.
    Returns appropriate success messages and user data, or an empty list if no users exist.
    """

    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        user_serializer = self.serializer_class(data=request.data)
        if not user_serializer.is_valid(raise_exception=True):
            return Response({"success": False, 'message': user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        user_serializer.save()
        return Response({"success": True, 'message': "User create successfully."}, status=status.HTTP_200_OK)


    def get(self, request, *args, **kwargs):
        user_obj = User.objects.all().order_by('-id')
        if not user_obj.exists():
            return Response({"success": True, 'data': []}, status=status.HTTP_200_OK)

        user_serializer = self.serializer_class(user_obj, many=True)

        response_dict = {
            "success": True,
            'data': user_serializer.data,
        }
        return Response(response_dict, status=status.HTTP_200_OK)


class UpdateDeleteUserView(APIView):
    """
    APIView for updating and deleting User objects based on user ID (pk).
    PUT updates user details, while DELETE removes a user, with a check to prevent deletion of admin users.
    Returns appropriate success or error messages and status codes based on the operation outcome.
    """

    serializer_class = UserSerializer

    def put(self, request, pk, *args, **kwargs):
        
        user_instance = get_object_or_404(User, id=pk)
        
        user_serializer = self.serializer_class(user_instance, data=request.data, partial=True, context={'request': request})
        if not user_serializer.is_valid(raise_exception=True):
            return Response({"success": False, "message": "User data not updated.", "errors": user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        user_serializer.save()
        
        return Response({"success": True, 'message': 'User updated successfully.'}, status=status.HTTP_200_OK)
    
    def delete(self, request, pk, *args, **kwargs):
        user_instance = get_object_or_404(User, id=pk)
        if user_instance.role == 'admin':
            return Response({"success": False, 'message': 'Admin user cannot be deleted.'}, status=status.HTTP_200_OK)
        user_instance.delete()
        return Response({"success": True, 'message': 'User deleted successfully.'}, status=status.HTTP_200_OK)
    
