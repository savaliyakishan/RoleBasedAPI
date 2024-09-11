# jwt
from jwt import decode

# django
from django.http import JsonResponse

# model
from user_management.models import User

# other
from datetime import datetime
import re


class AdminOnlyMiddleware:
    """
    Middleware to check if the user is an admin before accessing certain routes.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_pattern = r'^/api/v1/users(/\d+)?/?$'    
        entries_pattern = r'^/api/v1/entries(/\d+)?/?$'    
        
        if re.match(user_pattern, request.path):
            is_valid_user_token = self.decode_auth_token(request.headers.get('Authorization'))
            if isinstance(is_valid_user_token, JsonResponse):
                return is_valid_user_token
            request.user = is_valid_user_token
        
            if request.user.role != 'admin':
                return JsonResponse({"success": False, 'message': "Admin access required."}, status=403)
        
        if re.match(entries_pattern, request.path):
            is_valid_user_token = self.decode_auth_token(request.headers.get('Authorization'))
            if isinstance(is_valid_user_token, JsonResponse):
                return is_valid_user_token
            request.user = is_valid_user_token
            
            if request.method in ['POST', 'PUT'] and request.user.role not in ['admin', 'editor']:
                return JsonResponse({"success": False, 'message': "Admin Or Editor access required."}, status=403)
            
            if request.method in ['DELETE'] and request.user.role != 'admin':
                return JsonResponse({"success": False, 'message': "Admin access required."}, status=403)

        return self.get_response(request)


    def decode_auth_token(self, auth_header):
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({"success": False, 'message': "Authorization header not provided or not in the correct format."}, status=403)
        
        access_token = auth_header.split(' ')[1]
        decoded_token = decode(access_token, options={"verify_signature": False}, algorithms=['HS256'])

        current_time = datetime.utcnow().timestamp()
        if int(current_time) >= decoded_token['exp']:
            return JsonResponse({"success": False, 'message': "Token expired."}, status=403)

        user_id = decoded_token.get('user_id')
        if not user_id:
            return JsonResponse({"success": False, 'message': "Invalid token payload."}, status=403)

        user_obj = User.objects.filter(id=user_id).first()
        if not user_obj:
            return JsonResponse({"success": False, 'message': "The user does not exist."}, status=403)
            
        if not user_obj.is_active:
            return JsonResponse({"success": False, 'message': "Your account is not activated."}, status=403)
    
        if not user_obj.is_authenticated:
            return JsonResponse({"success": False, 'message': "User not Authenticated."}, status=403)
    
        return user_obj
