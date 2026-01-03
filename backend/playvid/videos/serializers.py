from rest_framework import serializers
from users.models import CustomUser, Channel
from .models import Videos, Comment, Tag


class VideosSerializer:
    ...