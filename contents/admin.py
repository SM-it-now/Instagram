from django.contrib import admin
from .models import Content, Image, FollowRelation


# Register your models here.
class ImageInline(admin.TabularInline):
    model = Image


# Content모델이 Image모델의 상위호환이 되게끔 inlines에 Imageline를 추가.
class ContentAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ('user', 'created_at', 'text',)


class FollowRelationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Content, ContentAdmin)
admin.site.register(Image)
admin.site.register(FollowRelation, FollowRelationAdmin)
