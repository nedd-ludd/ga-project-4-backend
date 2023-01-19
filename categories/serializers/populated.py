from .common import CategorySerializer
from items.serializers import ItemSerializer


class PopulatedCategorySerializer(CategorySerializer):
  #TODO secure tis
    items = ItemSerializer(many=True)


