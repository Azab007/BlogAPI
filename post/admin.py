from django.contrib import admin

from post.models import *


admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Image)
admin.site.register(Attachment)
admin.site.register(Comment)

