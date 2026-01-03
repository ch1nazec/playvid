from django.db import models
from django.core.validators import FileExtensionValidator
from users.models import Channel, CustomUser


# Create your models here.
class Tag(models.Model):
    name_tag = models.TextField(max_length=10_000, unique=True, blank=True)

class Videos(models.Model):
    channel_id = models.ForeignKey(Channel, related_name='channel', on_delete=models.CASCADE)
    name = models.CharField(max_length=150, blank=False)
    description = models.TextField(max_length=3000)
    preview = models.ImageField(upload_to='Channels/PreviewVideo/')
    video = models.FileField(upload_to='Channels/Video/%Y/%m/%d/', validators=[FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mov', 'mkv'])])
    like_score = models.PositiveIntegerField(default=0)
    dislike_score = models.PositiveIntegerField(default=0)
    repost_score = models.PositiveIntegerField(default=0)
    tag_list = models.ManyToManyField(Tag, related_name='tags', blank=True)


class Comment(models.Model):
    video = models.ForeignKey(Videos, related_name='video_comment', on_delete=models.CASCADE)
    users = models.ForeignKey(CustomUser, related_name='users_comment', on_delete=models.CASCADE)
    
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    
    like_score = models.PositiveIntegerField(default=0)
    dislike_score = models.PositiveIntegerField(default=0)
