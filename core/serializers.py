from rest_framework import serializers 
from .models import User , Room , Rating , Comment
from django.contrib.auth import get_user_model

User = get_user_model()  

class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

    def validate(self, data):
        if data['password'] == None:
            raise serializers.ValidationError({"password": "Check Your Password."})
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data, password=password)
        return user

class UserSerializer(serializers.ModelSerializer) :
    class Meta :
        model  = User
        fields = ("username","email",)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

class RoomSerializer(serializers.ModelSerializer) :
    owner = UserSerializer()
    class Meta :
        model = Room
        fields = ("id","name","about","image","owner","members","rating",)

class CreateRoomSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Room
        fields = ("name","about","image",)

class JoinRoomSerializer(serializers.Serializer):
    room_id = serializers.IntegerField()


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['room', 'rate']

class CreateRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['room', 'rate']

    def validate(self, value):
        if not (1 <= value["rate"] <= 5):  
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

class CommentSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Comment
        fields = ["user","room","body"]

    def validate(self, attrs):
        if attrs["body"] == None :
            raise serializers.ValidationError("you can't post an empty comment..")
        return attrs         

