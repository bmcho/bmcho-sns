from rest_framework import serializers

from apps.hashtag.serializers import HashtagsSerializer
from apps.review.serializers import ReviewSerializers
from apps.user.serializers import UserSerializer

from .models import Post, PostLike


class PostCreateCheckSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50)
    contents = serializers.CharField(allow_blank=False)
    hashtag = serializers.CharField()


class PostSerializer(serializers.ModelSerializer):
    """게시글 작성, 수정 serializer

    Writer: 조병민
    Date: 2022-07-22
    """

    user = UserSerializer(read_only=True)
    title = serializers.CharField(max_length=50)
    contents = serializers.CharField(allow_blank=False)
    hashtag = serializers.SlugRelatedField(many=True, read_only=True, slug_field="hashtag_name")

    def create(self, validated_data):
        user = self.context.get('user')
        hashtag = self.context.get('hashtag')

        instance = Post.objects.create(user=user, title=validated_data['title'], contents=validated_data['contents'])

        for h in hashtag:
            hashtag_serializer = HashtagsSerializer(data={'hashtag_name': h})

            hashtag_serializer.is_valid(raise_exception=True)
            hashtag_obj = hashtag_serializer.save()
            instance.hashtag.add(hashtag_obj)

        return instance

    def update(self, instance, validated_data):
        instance = super(PostSerializer, self).update(instance, validated_data)
        instance.save()
        return instance

    class Meta:
        model = Post
        fields = ['user', 'id', 'title', 'contents', 'hashtag']


class PostSearchSerializer(serializers.ModelSerializer):
    """게시글 검색 serializer

    Writer: 조병민
    Date: 2022-07-24
    """

    user = UserSerializer(read_only=True)
    title = serializers.CharField()
    hashtag = serializers.SlugRelatedField(many=True, read_only=True, slug_field="hashtag_name")
    like = serializers.SerializerMethodField()

    def get_like(self, instance):
        return instance.like.count()

    class Meta:
        model = Post
        fields = ['user', 'id', 'title', 'hashtag', 'like', 'created_at']


class PostDetailSearchSerializer(serializers.ModelSerializer):
    """게시글 상세 검색 serializer

    Writer: 조병민
    Date: 2022-07-24
    """

    user = UserSerializer(read_only=True)
    title = serializers.CharField()
    contents = serializers.CharField()
    hashtag = serializers.SlugRelatedField(many=True, read_only=True, slug_field="hashtag_name")
    like = serializers.SerializerMethodField()
    reviews = ReviewSerializers(many=True)

    def get_like(self, instance):
        return instance.like.count()

    class Meta:
        model = Post
        fields = ['user', 'id', 'title', 'contents', 'hashtag', 'like', 'hits', 'reviews', 'created_at']


class PostLikeSerializer(serializers.ModelSerializer):
    """게시글 좋아요 생성 serializer

    Writer: 조병민
    Date: 2022-07-24
    """

    def create(self, validated_data):
        instans = PostLike.objects.create(**validated_data)
        return instans

    class Meta:
        model = PostLike
        fields = ['user', 'post']
