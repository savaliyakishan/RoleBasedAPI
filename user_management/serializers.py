# drf
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

# model
from user_management.models import User

# base
from base.base_helper import GlobalHelperFunction, validate_password


class UserSerializer(serializers.ModelSerializer, GlobalHelperFunction):
    
    """
    Serializer for the User model with validation and custom create/update behavior.
    Validates username length, password strength, and uniqueness of the username.
    Handles password encryption on user creation and updates, and allows updating username and role.
    """

    username = serializers.CharField(required=False, allow_blank=True)
    role = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(required=False, allow_blank=True, write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'password']
        read_only = ('id',)
        write_only = ('password',)

    def validate(self, data):
        username  = data.get('username', None)
        role  = data.get('role', None)
        password  = data.get('password', None)

        # validation
        self.value_list = {"Username": username, "Role":role, "Password":password}
        self.validations()
        if self.Response:
            raise ValidationError(f"{self.key} field is required.", code=400)
    
        if len(username) > 150:
            raise ValidationError("Username must be 150 characters or fewer.", code=400)

        # password validation
        check_password = validate_password(password)
        if not check_password: raise ValidationError("String must contain at least 8 characters, including one uppercase letter, one lowercase letter, one digit, and one special character.", code = 400)

        # check role
        valid_roles = [role[0] for role in User.ROLE_CHOICES]
        if role not in valid_roles:
            raise ValidationError("Provide valid role in admin, editor or user.", code = 400)

        # check user exist
        user_obj = User.objects.filter(username=username)
        
        # update time
        if self.instance:
            user_obj = user_obj.exclude(username=self.instance.username)
        
        if user_obj.exists():
            raise ValidationError("Username already exists.", code=400)
               
        return super().validate(data)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        role = validated_data.get('role', None)
        if role:
            instance.role = role
        if validated_data.get('password'):
            instance.set_password(validated_data['password'])
        instance.save()
        return instance
