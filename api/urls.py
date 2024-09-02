from django.urls import path
from .views import (
    RegisterView, UserSearchView, SendFriendRequestView,
    AcceptFriendRequestView, RejectFriendRequestView,
    FriendsListView, PendingRequestsView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('users/search/', UserSearchView.as_view(), name='user-search'),
    path('friend-request/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('friend-request/accept/', AcceptFriendRequestView.as_view(), name='accept-friend-request'),
    path('friend-request/reject/', RejectFriendRequestView.as_view(), name='reject-friend-request'),
    path('friends/', FriendsListView.as_view(), name='friends-list'),
    path('friend-requests/pending/', PendingRequestsView.as_view(), name='pending-friend-requests'),
]
