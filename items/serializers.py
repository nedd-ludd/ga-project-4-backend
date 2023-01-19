from rest_framework import serializers
from .models import Item
from categories.serializers.common import CategorySerializer
# from artists.serializers.common import ArtistSerializer
# todo user serializer

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item  # the model our ser.. will use to transform
        fields = '__all__'  # specify what fields we want to return


class PopulatedItemSerializer(ItemSerializer):
    categories = CategorySerializer(many=True)
