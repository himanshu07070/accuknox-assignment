from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import FriendRequest
from .serializers import UserSerializer, RegisterSerializer, FriendRequestSerializer
from .throttles import BurstRateThrottle
from rest_framework.permissions import IsAuthenticated

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = []

class UserSearchView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']

class SendFriendRequestView(APIView):
    throttle_classes = [BurstRateThrottle]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        to_user = User.objects.get(id=request.data['to_user_id'])
        friend_request, created = FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user)
        if created:
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Friend request already sent"}, status=status.HTTP_400_BAD_REQUEST)

class AcceptFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        friend_request = FriendRequest.objects.get(id=request.data['request_id'])
        if friend_request.to_user == request.user:
            friend_request.status = 'accepted'
            friend_request.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class RejectFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        friend_request = FriendRequest.objects.get(id=request.data['request_id'])
        if friend_request.to_user == request.user:
            friend_request.status = 'rejected'
            friend_request.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class FriendsListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        friends = User.objects.filter(
            models.Q(sent_requests__to_user=user, sent_requests__status='accepted') |
            models.Q(received_requests__from_user=user, received_requests__status='accepted')
        )
        return friends

class PendingRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, status='pending')
