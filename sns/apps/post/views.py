from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.hashtag.serializers import HashtagsSerializer

from .models import Post
from .serializers import PostSerializer


# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        request_get_hashtag = data.pop('hashtag')
        try:
            new_post = Post.objects.create(user=user, title=data['title'], contents=data['contents'])
            new_post.save()

            if request_get_hashtag:
                for h in request_get_hashtag:
                    hashtag_serializer = HashtagsSerializer(data={'hashtag_name': h})

                    hashtag_serializer.is_valid(raise_exception=True)
                    hashtag_obj = hashtag_serializer.save()
                    new_post.hashtag.add(hashtag_obj)

            serializer = PostSerializer(new_post)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            print(ex)
            raise APIException(detail='error occurred', code=ex)
