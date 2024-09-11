# drf
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

# model
from entry_management.models import Entry

# base
from base.base_helper import GlobalHelperFunction, validate_email


class EntrySerializer(serializers.ModelSerializer, GlobalHelperFunction):
    """
    Serializer for Entry model that includes optional name, email, and comments fields.
    Validates the length of the name and the format of the email using custom helper functions.
    Raises ValidationError for invalid input or missing required fields.
    """


    name = serializers.CharField(required=False, allow_blank=True)
    email = serializers.CharField(required=False, allow_blank=True)
    comments = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = Entry
        fields = ['id', 'name', 'email', 'comments']
        read_only = ('id',)

    def validate(self, data):
        name  = data.get('name', None)
        email  = data.get('email', None)
        comments  = data.get('comments', None)

        # Validation
        self.value_list = {"Name": name, "Email":email, "Comments":comments}
        self.validations()
        if self.Response:
            raise ValidationError(f"{self.key} field is required.", code=400)
    
        if len(name) > 255:
            raise ValidationError("Username must be 255 characters or fewer.", code=400)

        # password validation
        check_email = validate_email(email)
        if not check_email: raise ValidationError("Please enter a valid email address.", code = 400)

        return super().validate(data)
