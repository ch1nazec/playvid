from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
# class Tag(models.Model):
#     name_tag = models.TextField(max_length=10_000, unique=True, blank=True)


class CustomUser(AbstractUser):
    phone_number = PhoneNumberField(region='RU')


class Channel(models.Model):
    user_id = models.OneToOneField(CustomUser, related_name='user', on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='Channels/AvatarChannel/%Y/%m/%d/', blank=True)
    channel_name = models.CharField(max_length=100, blank=False, unique=True)
    slug_name = models.SlugField(max_length=100, blank=False, unique=True)
    created_date = models.DateField(auto_now_add=True, editable=False)
    description = models.TextField()
    preview = models.ImageField(upload_to='Channels/PreviewsChannel/%Y/%m/%d/')
    
    def save(self, *args, **kwargs):
        if not self.slug_name:
            self.slug_name = slugify()
        return super().save(*args, **kwargs)


# class Videos(models.Model):
#     channel_id = models.ForeignKey(Channel, related_name='channel', on_delete=models.CASCADE)
#     name = models.CharField(max_length=150, blank=False)
#     description = models.TextField(max_length=3000)
#     preview = models.ImageField(upload_to='Channels/PreviewVideo/')
#     video = models.FileField(upload_to='Channels/Video/%Y/%m/%d/', validators=[FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mov', 'mkv'])])
#     like_score = models.PositiveIntegerField(default=0)
#     dislike_score = models.PositiveIntegerField(default=0)
#     repost_score = models.PositiveIntegerField(default=0)
#     tag_list = models.ManyToManyField(Tag, related_name='tags', blank=True)


# class Comment(models.Model):
#     video = models.ForeignKey(Videos, related_name='video_comment', on_delete=models.CASCADE)
#     users = models.ForeignKey(CustomUser, related_name='users_comment', on_delete=models.CASCADE)
    
#     text = models.TextField(max_length=1000)
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     like_score = models.PositiveIntegerField(default=0)
#     dislike_score = models.PositiveIntegerField(default=0)