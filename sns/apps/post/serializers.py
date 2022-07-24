from rest_framework import serializers

from apps.hashtag.serializers import HashtagsSerializer
from apps.user.serializers import UserSerializer

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    """게시글 작성, 수정 serializer

    Writer: 조병민
    Date: 2022-07-22
    """

    user = UserSerializer(read_only=True)
    title = serializers.CharField(max_length=50)
    contents = serializers.CharField(allow_blank=False)
    hashtag = serializers.SlugRelatedField(many=True, read_only=True, slug_field="hashtag_name")

    def update(self, instance, validated_data):
        instance = super(PostSerializer, self).update(instance, validated_data)
        instance.save()
        return instance

    class Meta:
        model = Post
        fields = ['user', 'id', 'title', 'contents', 'hashtag']
