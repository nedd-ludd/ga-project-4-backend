from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers.populated import PopulatedCategorySerializer
from .models import Category


class CategoryListView(APIView):
    def get(self, _request):
        catgories = Category.objects.all()
        serialized_catgories = PopulatedCategorySerializer(catgories, many=True)
        return Response(serialized_catgories.data, status=status.HTTP_200_OK)


class CategoryDetailView(APIView):
    def get(self, _request, pk):
        category = Category.objects.get(pk=pk)
        serialized_category = PopulatedCategorySerializer(category)
        return Response(serialized_category.data, status=status.HTTP_200_OK)
