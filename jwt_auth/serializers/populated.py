from .common import UserSerializer
from items.serializers import ItemSerializer


class PopulatedUserSerializer(UserSerializer):
  #TODO secure tis
    items = ItemSerializer(many=True)



