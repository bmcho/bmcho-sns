from django.db import transaction
from rest_framework import decorators, status, viewsets
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

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

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

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        post_obj = self.queryset.filter(id=kwargs['post_id'], user=user).get()

        if not post_obj:
            return Response({'detail': 'not the author'}, status=status.HTTP_401_UNAUTHORIZED)

        request_get_hashtag = data.pop('hashtag')
        try:
            serializer = PostSerializer(post_obj, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            modi_post = serializer.save()
            modi_post.hashtag.clear()
            if request_get_hashtag:
                for h in request_get_hashtag:
                    hashtag_serializer = HashtagsSerializer(data={'hashtag_name': h})

                    hashtag_serializer.is_valid(raise_exception=True)
                    hashtag_obj = hashtag_serializer.save()
                    modi_post.hashtag.add(hashtag_obj)

            serializer = PostSerializer(modi_post)

            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except Exception as ex:
            print(ex)
            raise APIException(detail='error occurred', code=ex)

    def list(self, request):
        a = PostSerializer(self.queryset[10:], many=True)
        return Response({'data': a.data}, status=status.HTTP_200_OK)
