from importlib.metadata import requires

from rest_framework import serializers

from apps.review.models import Review


class ReivewCreateCheckSerializers(serializers.Serializer):
    review = serializers.CharField(required=True)


class ReivewUpdateCheckSerializers(serializers.Serializer):
    review_id = serializers.IntegerField(required=True)
    review = serializers.CharField(required=True)


class ReivewDeleteCheckSerializers(serializers.Serializer):
    review_id = serializers.IntegerField(required=True)


class ReviewSerializers(serializers.ModelSerializer):
    post_id = serializers.IntegerField(required=True)
    user_id = serializers.IntegerField(required=True)
    review = serializers.CharField(required=True)

    def create(self, validated_data):
        instance = Review.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        instance.review = validated_data.get('review', instance.review)
        instance.save()

        return instance

    class Meta:
        model = Review
        fields = ['id', 'post_id', 'user_id', 'review', 'created_at']
