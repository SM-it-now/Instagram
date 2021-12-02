import os
import uuid

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# 다른 클래스에 기본으로 상속되는 base모델.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Content 모델 생성
class Content(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:
        ordering = ['-created_at']


# 사용자가 업로드 한 이미지의 네임을 그대로 사용하지 않고, 16자리의 고유한 아이디를 생성. --> uuid
def image_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.join(instance.UPLOAD_PATH, "%s.%s" %(uuid.uuid4(), ext))


# Image 모델 생성
class Image(BaseModel):
    UPLOAD_PATH = 'user-upload'

    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_upload_to)
    order = models.SmallIntegerField() # 이미지 순서를 위한 필드

    class Meta:
        unique_together = ['content', 'order']
        ordering = ['order']


# 팔로우 관계 모델
class FollowRelation(BaseModel):
    follower = models.OneToOneField(User, on_delete=models.CASCADE, related_name='follower')
    followee = models.ManyToManyField(User, related_name='followee')


