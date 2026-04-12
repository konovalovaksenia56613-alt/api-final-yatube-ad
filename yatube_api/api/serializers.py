from django.contrib.auth import get_user_model
from rest_framework import serializers
from posts.models import Post, Group, Comment, Follow

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'text', 'pub_date', 'author', 'image', 'group')

    def get_author(self, obj):
        return obj.author.username


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('post',)

    def get_author(self, obj):
        return obj.author.username


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def get_user(self, obj):
        return obj.user.username

    def validate_following(self, value):
        if self.context['request'].user == value:
            raise serializers.ValidationError('Нельзя подписаться на себя')
        if Follow.objects.filter(
            user=self.context['request'].user,
            following=value
        ).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя'
            )
        return value
