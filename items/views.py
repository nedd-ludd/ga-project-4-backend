from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from django.db import IntegrityError
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Item
from .serializers import ItemSerializer, PopulatedItemSerializer

# from ..helpers import is_owner

class ItemListView(APIView):
    
    permission_classes = (IsAuthenticatedOrReadOnly, )
    def get(self, _request):
        items = Item.objects.all() 
        serialized_items = ItemSerializer(items, many=True)
        return Response(serialized_items.data, status=status.HTTP_200_OK)

    def post(self, request):
        print(request.data)
        request.data['owner'] = request.user.id
        item_to_add = ItemSerializer(data=request.data)
        try:
            item_to_add.is_valid()
            item_to_add.save()
            return Response(item_to_add.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            res = {
                "detail": str(e)
            }
            return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except AssertionError as e:
            return Response({"details": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({"detail": "Unprocessable Entitry"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ItemDetailView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_item(self, pk):
        try:
            return Item.objects.get(pk=pk)
        except:
            raise NotFound(detail="Can't find that item")

    def get(self, _request, pk):
        # ! check whether owned by friend OR owned by self
        item = self.get_item(pk=pk)
        serialized_item = PopulatedItemSerializer(item)
        return Response(serialized_item.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        request.data['owner'] = request.user.id
        item_to_edit = self.get_item(pk=pk)
        updated_item = ItemSerializer(item_to_edit, data=request.data)
        try:
            updated_item.is_valid()
            updated_item.save()
            return Response(updated_item.data, status=status.HTTP_202_ACCEPTED)
        except AssertionError as e:
            print("here")
            return Response({"detail": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({"detail": "Unprocessible Entity"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request, pk):
        item_to_delete = self.get_item(pk=pk)
        serialized_item = ItemSerializer(item_to_delete)
        try:
          if request.user.id != serialized_item.data["owner"]:
            raise PermissionDenied
        except PermissionDenied:
          return Response({"detail": "You do not have permission to perform that action"}, status=status.HTTP_401_UNAUTHORIZED)
        item_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ItemSearchView(APIView):
  def get(self, request):
    search_query = request.GET.get("search")
    print("searching for", search_query)
    results = Item.objects.filter(name__icontains=search_query)
    serialized_results = ItemSerializer(results, many=True)
    return Response(serialized_results.data)

class ItemPullUserView(APIView):
  def get(self, request):

    search_query = request.GET.get("search")
    print("gettin items from user", search_query)
    results = Item.objects.filter(owner=search_query)
    serialized_results = ItemSerializer(results, many=True)
    return Response(serialized_results.data)

