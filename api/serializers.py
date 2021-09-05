from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile, Post, Comment

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    # get_user_model:現時点で有効になっているUserモデル自体を呼び出す
    model = get_user_model()
    fields = (
      'id',
      'email',
      'password'
    )
    extra_kwargs= {
      'password': {
        'write_only': True
      }
    }

  def create(self, validated_data):
    # validated_data:バリデーション後の値が格納されている。バリデーションが失敗すると空になる
    user = get_user_model().objects.create_user(**validated_data)
    return user

class ProfileSerializer(serializers.ModelSerializer):
  # created_atをoverrideする
  created_at = serializers.DateTimeField(
    format="%Y-%m-%d",
    read_only=True
  )
  class Meta:
    model=Profile
    fields = (
      'id',
      'userName',
      'userProfile',
      'created_at',
      'img'
    )
    extra_kwargs = {
      'userProfile': {
        'read_only': True
      }
    }

class PostSerializer(serializers.ModelSerializer):
  # created_atをoverrideする
  created_at = serializers.DateTimeField(
    format="%Y-%m-%d",
    read_only=True
  )
  class Meta:
    model = Post
    fields = (
      'id',
      'title',
      'postedUser',
      'created_at',
      'img',
      'liked'
    )
    extra_kwargs = {
      'postedUser': {
        'read_only': True
      }
    }

class CommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = (
      'id',
      'text',
      'commentedUser',
      'post'
    )
    extra_kwargs = {
      'commentedUser': {
        'read_only': True
      }
    }