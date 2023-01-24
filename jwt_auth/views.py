from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound, PermissionDenied
# this can create timestamps in different formats
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.conf import settings
import jwt

from .serializers.common import UserSerializer
from .serializers.populated import PopulatedUserSerializer

User = get_user_model()


class RegisterView(APIView):
    def post(self, request):
        user_to_create = UserSerializer(data=request.data)
        print(request.data)
        if user_to_create.is_valid():
            user_to_create.save()
            return Response({'message': "Registration Successful"}, status=status.HTTP_201_CREATED)
        return Response(user_to_create.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class LoginView(APIView):
    def post(self, request):
        # get the data from the request
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user_to_login = User.objects.get(email=email)
        except User.DoesNotExist:
            raise PermissionDenied(detail='Invalid Credentials')
        if not user_to_login.check_password(password):
            raise PermissionDenied(detail='Invalid Credentials')

        dt = datetime.now() + timedelta(days=7)  # how long the token will be valid for

        token = jwt.encode(
            {'sub': user_to_login.id},
            settings.SECRET_KEY,
            algorithm='HS256'
        )

        return Response({'token': token, 'message': f"Welcome back {user_to_login.username}"})

class UserListView(APIView):
  permission_classes = (IsAuthenticatedOrReadOnly, )

  def get(self, _request):
    users = User.objects.all()
    serialized_users = UserSerializer(users, many=True)
    return Response(serialized_users.data, status=status.HTTP_200_OK)

class UserDetailView(APIView):
  permission_classes=(IsAuthenticatedOrReadOnly,)
  #!could investigate different classes for this once got functionality in
  def get_user(self, pk):
      try:
        return User.objects.get(pk=pk)
      except:
          raise NotFound(detail="Can't find that user")

  def get(self, _request, pk):
  #   # todo do I need serialisers:
  #   # populated, non user truncated view
    user = self.get_user(pk=pk)
    serialized_user = PopulatedUserSerializer(user)
  #   #todo populated for items
    return Response(serialized_user.data, status=status.HTTP_200_OK)

  def put(self, request, pk):
    user_to_edit = self.get_user(pk=pk)
    serialized_user = UserSerializer(user_to_edit)
    try:
      if request.user.id != serialized_user.data["id"]:
        raise PermissionDenied
    except PermissionDenied:
      return Response({"detail": "You do not have permission to perform that action"}, status=status.HTTP_401_UNAUTHORIZED)

    updated_user =UserSerializer(user_to_edit, data=request.data)
    try:
      updated_user.is_valid()
      updated_user.save()
      return Response(updated_user.data, status=status.HTTP_202_ACCEPTED)
    except AssertionError as e:
      return Response({"detail": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except:
      return Response({"detail": "Unprocessible Entity"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)



  def delete(self, request, pk):
    user_to_delete = self.get_user(pk=pk)
    serialized_user = UserSerializer(user_to_delete)
    try:
        if request.user.id != serialized_user.data["id"]:
          raise PermissionDenied
    except PermissionDenied:
        return Response({"detail": "You do not have permission to perform that action"}, status=status.HTTP_401_UNAUTHORIZED)
    user_to_delete.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)