from rest_framework import serializers
from .models import Friendship
from items.serializers import ItemSerializer
# from artists.serializers.common import ArtistSerializer
# todo user serializer

class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship  # the model our ser.. will use to transform
        fields = '__all__'  # specify what fields we want to return


class PopulatedFriendshipSerializer(FriendshipSerializer):
    items = ItemSerializer(many=True)
