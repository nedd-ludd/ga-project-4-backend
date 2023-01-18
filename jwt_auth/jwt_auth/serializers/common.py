from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation
# we can use this to hash passwords when a user is registered
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    # when the User is being converted back to JSON to return data to the user, password and password_confirmation are not going to be returned.
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    # validate function is going to:
    # check password matches password_confirmation
    # hash the password
    # update the password on the data object that is passed through from the request in the views
    def validate(self, data):
        # get the fields we need for the password stuff and save as variables
        password = data.pop('password')
        password_confirmation = data.pop('password_confirmation')

        if password != password_confirmation:
            raise ValidationError(
                {'password_confirmation': 'Passwords do not match'})

        # make sure the password is valid
        try:
            password_validation.validate_password(password=password)
        except ValidationError as err:
            raise ValidationError({'password': err.messages})

        # if password is valid, reassign the value of data.password to the hashed password
        data['password'] = make_password(password)

        return data  # return the updated data dictionary with hashed password

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'profile_image', 'password', 'password_confirmation')
