from django.urls import path
from .views import FriendshipListView

urlpatterns = [
    path('', FriendshipListView.as_view()),
] 