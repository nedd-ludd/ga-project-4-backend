from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from django.db import IntegrityError
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Friendship
from .serializers import FriendshipSerializer, PopulatedFriendshipSerializer


class FriendshipListView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, _request):
        friendships = Friendship.objects.all() 
        serialized_friendships = FriendshipSerializer(friendships, many=True)
        return Response(serialized_friendships.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data['user_one'] = request.user.id
        friendship_to_add = FriendshipSerializer(data=request.data)
        try:
            friendship_to_add.is_valid()
            friendship_to_add.save()
            return Response(friendship_to_add.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            res = {
                "detail": str(e)
            }
            return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except AssertionError as e:
            return Response({"details": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({"detail": "Unprocessable Entitry"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
