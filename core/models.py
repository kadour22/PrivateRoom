from django.db import models
from django.contrib.auth.models import BaseUserManager , AbstractBaseUser , PermissionsMixin
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            email = self.normalize_email(email)
        username = username
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    
    username   = models.CharField(max_length=255 , unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name  = models.CharField(max_length=150, blank=True)
    email      = models.EmailField(blank=True)
    is_staff   = models.BooleanField(default=False)
    is_active  = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username

class Room(models.Model) :
    name  = models.CharField(max_length=255)
    about = models.TextField()
    image = models.ImageField(upload_to="rooms")

    owner   = models.ForeignKey(User , on_delete=models.CASCADE , related_name="rooms" )
    members = models.ManyToManyField(User)

    def __str__(self):
        return f"Room Name : {self.name} Created By :{self.owner.username}" 


class Rating(models.Model) :
    room = models.ForeignKey(Room , on_delete= models.CASCADE , related_name="rating")
    user = models.ForeignKey(User , on_delete= models.CASCADE , related_name="rating")
    rate = models.IntegerField()


    class Meta:
        unique_together = ('room', 'user',)

    def __str__(self) :
        return f"{self.room} rated by : {self.user}"    

class Comment(models.Model) :
    room = models.ForeignKey(Room , on_delete= models.CASCADE , related_name="comments")
    user = models.ForeignKey(User , on_delete= models.CASCADE , related_name="comments")
    body = models.TextField()

    def __str__(self) :
        return f"{self.room} {self.user}"


class ReplayComment(models.Model) :
    comment = models.ForeignKey(Comment , on_delete= models.CASCADE , related_name="replay")
    user    = models.ForeignKey(User    , on_delete= models.CASCADE , related_name="replay")
    
    body    = models.TextField()

    def __str__(self) :
        return f"{self.comment.body} => {self.body}"
    