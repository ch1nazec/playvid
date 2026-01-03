from django.db import models
from django.core.validators import FileExtensionValidator
from users.models import Channel
from mptt.models import MPTTModel, TreeForeignKey


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


class Comment(MPTTModel):
    video = models.ForeignKey(Videos, related_name='comments', on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, related_name='children', db_index=True)
    
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_hidden = models.BooleanField(default=False)
    
    class MPTTMeta:
        order_insertion_by = ['created_at']
        
    class Meta:
        indexes = [
            models.Index(fields=['video', 'created_at',]),
            models.Index(fields=['video', 'parent',]),
        ]
        ordering = ['-created_at']
    
    @property
    def reply_count(self):
        return self.children.count()
    
    def __str__(self):
        return f"{self.channel.channel_name}'s comment"