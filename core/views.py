from rest_framework import generics , status , permissions
from rest_framework.views import  APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin

from .models import User , Room  , Rating ,Comment
from .serializers import (
    CreateRoomSerializer,
    RoomSerializer ,
    JoinRoomSerializer,
    UserRegistrationSerializer , 
    LoginSerializer , 
    CommentSerializer , 
    RatingSerializer , 
    CreateRatingSerializer,
    )
from .permissions import IsRoomMember , IsRoomOwner
from .throttling import OneTimeRatingThrottle , CommentThrottle
# from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import authenticate , login


class RoomListView(generics.ListAPIView) :
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    permission_classes = [permissions.AllowAny]


class CreateRoomView(generics.CreateAPIView) :
    serializer_class = CreateRoomSerializer
    queryset = Room.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self , serializer) :
        serializer.save(owner = self.request.user)

class DetailRoomView(generics.RetrieveAPIView) :
    serializer_class = CreateRoomSerializer
    queryset = Room.objects.all()
    permission_classes = [IsRoomMember]
    lookup_field = "id"

class UpdateRoomView(generics.UpdateAPIView) :
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    permission_classes = [IsRoomOwner]
    lookup_field = "id"

class JoinRoomAPIView(GenericAPIView, CreateModelMixin):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = JoinRoomSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            room_id = serializer.validated_data['room_id']
            user = request.user
            
            try:
                room = Room.objects.get(id=room_id)
            except Room.DoesNotExist:
                return Response({"detail": "Room not found."}, status=status.HTTP_404_NOT_FOUND)

            if user in room.members.all():
                return Response({"detail": "You are already a member of this room."}, status=status.HTTP_400_BAD_REQUEST)

            room.members.add(user)
            room.save()
            
            return Response({"detail": "Successfully joined the room."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserRegisterView(generics.CreateAPIView) :
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

class RatingView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [OneTimeRatingThrottle]
    def post(self, request):
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            room_id = serializer.validated_data['room']
            rating_value = serializer.validated_data['rate']
            
            room = Room.objects.get(id=room_id)
            user = request.user

            # Check if the user has already rated this room
            rating, created = Rating.objects.get_or_create(room=room, user=user, defaults={'rating': rating_value})
            if not created:
                # Update rating if it already exists
                rating.rating = rating_value
                rating.save()
            
            return Response({'detail': 'Rating submitted successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self , request) :
        rates = Rating.objects.all()
        serializer = RatingSerializer(rates , many=True)
        return Response(serializer.data)


class Createrate(generics.ListCreateAPIView):
    serializer_class = CreateRatingSerializer
    queryset = Rating.objects.all()


class CommentView(generics.ListCreateAPIView) :
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    throttle_classes = [CommentThrottle]
    