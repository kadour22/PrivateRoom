from django.contrib import admin
from .models import User , Room , Rating , Comment , ReplayComment


admin.site.register(User)
admin.site.register(Room)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(ReplayComment)