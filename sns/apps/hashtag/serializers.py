from rest_framework import serializers

from .models import Hashtag


class HashtagsSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        hashtag_name = validated_data.get('hashtag_name')

        if Hashtag.objects.filter(hashtag_name=hashtag_name):
            return Hashtag.objects.filter(hashtag_name=hashtag_name).first()
        else:
            return Hashtag.objects.create(**validated_data)

    class Meta:
        model = Hashtag
        fields = ['hashtag_name']
