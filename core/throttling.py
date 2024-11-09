from rest_framework.throttling import BaseThrottle
from .models import Rating , Comment

class OneTimeRatingThrottle(BaseThrottle):
    def allow_request(self, request, view):
        user = request.user
        room_id = request.data.get('room')
        
        if user.is_authenticated and room_id is not None:
            if Rating.objects.filter(user=user, room_id=room_id).exists():
                return False  # Throttle the request..

        return True


class CommentThrottle(BaseThrottle) :
    def allow_request(self, request, view):
        user = request.user 
        room_id = request.data.get('room') 

        if user.is_authenticated and room_id is not None :
            cmtr = Comment.objects.filter(user=user,room_id=room_id).count()

            if cmtr >= 2 :
                return False
        
        return True
