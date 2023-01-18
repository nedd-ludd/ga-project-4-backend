# Class to inherit that has pre-defined validations
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import PermissionDenied  # throws an exception
# method that returns the current auth model
from django.contrib.auth import get_user_model
# import settings so we can get secret key (we'll come back to this)
from django.conf import settings
import jwt  # import jwt so we can decode the token in the auth header

User = get_user_model()  # saving auth model to a variable


class JWTAuthentication(BasicAuthentication):

    # This will act as the middleware that authenticates our secure routes
    def authenticate(self, request):
        # Get the Authorization header from the incoming request object and save it to a variable.
        auth_header = request.headers.get('Authorization')

        # Check if header has a value. If it doesn't, return None.
        if not auth_header:
            return None

        # Check that the token starts with Bearer
        if not auth_header.startswith('Bearer'):
            raise PermissionDenied(detail="Invalid Auth Token Format")

        # remove Bearer from beginning of Authorization header
        token = auth_header.replace('Bearer ', '')

        # Get payload, take the sub (the user id) and make sure that user exists
        try:
            # 1st arg is the token itself
            # 2nd arg is the secret
            # 3rd argument is kwarg that takes the algorithm used
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])

            # find user
            user = User.objects.get(pk=payload.get('sub'))

        # if jwt.decode errors, this except will catch it
        except jwt.exceptions.InvalidTokenError:
            raise PermissionDenied(detail='Invalid Token')

        # If no user is found in the db matching the sub, the below will catch it
        except User.DoesNotExist:
            raise PermissionDenied(detail='User Not Found')

        # If all good, return the user and the token
        return (user, token)
