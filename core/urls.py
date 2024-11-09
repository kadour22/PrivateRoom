from django.urls import path
from . import views 
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView

urlpatterns = [
   
    # Rooms urls
    path("room-list/" , views.RoomListView.as_view(),name='room-list+'),
    path("room-create/" , views.CreateRoomView.as_view()),
    path("room-detail/<int:id>/" , views.DetailRoomView.as_view()),
    path("room-update/<int:id>/" , views.UpdateRoomView.as_view()),
    path('join/', views.JoinRoomAPIView.as_view()),

    # Users urls
    path('register/' , views.UserRegisterView.as_view()),
    path('token/' , TokenObtainPairView.as_view()),
    path('token/refresh/' , TokenRefreshView.as_view()),

    # Rating urls
    path("rate/" , views.RatingView.as_view()),
    # Comment urls
    path("comment/" , views.CommentView.as_view()),

]