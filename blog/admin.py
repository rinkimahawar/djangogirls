from django.contrib import admin
from .models import Post, User,Profile,Category


admin.site.register(Post)
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Category)
