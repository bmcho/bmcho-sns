from venv import create

from django.core.cache import cache
from django.db import transaction
from django.db.models import Count, Q
from rest_framework import status, viewsets
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.core.util import get_client_ip
from apps.hashtag.serializers import HashtagsSerializer

from .models import Post, PostLike
from .serializers import (
    PostCreateCheckSerializer,
    PostDetailSearchSerializer,
    PostLikeSerializer,
    PostSearchSerializer,
    PostSerializer,
)


# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    """게시글 CRUD ViewSet

    Write: 조병민
    Date: 2022-07-22

    GET: list ('') - 리스트 검색
        query_params = (search: 검색 키워드, page: 페이지, hashtag: 해시태그, author: 작성자, ordering: 정렬기준)
            ordering - default: -created_at
                       select : like, -like, created_at
    GET: retrieve ('/post_id') - 상세 검색
    POST: create ('') - 생성
    PATCH: partial_update ('/post_id') - 수정
    DELETE: destroy ('/post_id') - 삭제
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    __max_Page = 10

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        check_serializer = PostCreateCheckSerializer(data=request.data)
        check_serializer.is_valid(raise_exception=True)

        try:
            user = request.user
            data = request.data
            request_get_hashtag = data.pop('hashtag').replace('#', '').split(',')

            serializer = PostSerializer(
                data={
                    'title': data['title'],
                    'contents': data['contents'],
                },
                context={'user': user, 'hashtag': request_get_hashtag},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            print(ex)

            raise APIException(detail='error occurred', code=ex)

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        post_obj = self.queryset.filter(id=kwargs['post_id'], user=user)

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

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        user = request.user
        post_id = kwargs.get('post_id')

        try:
            post_obj = self.queryset.filter(id=post_id).first()

            if not post_obj:
                return Response({'detail': 'not existed post'}, status=status.HTTP_404_NOT_FOUND)

            post_obj = self.queryset.filter(id=kwargs.get('post_id'), user=user).first()

            if not post_obj:
                return Response({'detail': 'not the author'}, status=status.HTTP_401_UNAUTHORIZED)

            post_obj.delete()
            return Response({'detail': 'success, deleted post'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            print(ex)
            raise APIException(detail='error occurred', code=ex)

    def list(self, request, *args, **kwargs):
        # params
        page = int(request.GET.get('page', 1))
        search = request.GET.get('search', None)
        hashtag = request.GET.get('hashtag', None)
        ordering = request.GET.get('ordering', '-created_at')

        try:
            q = Q()
            offset, limite = (page - 1) * self.__max_Page, page * self.__max_Page

            if search:
                q_search = Q()
                q_search.add(Q(title__contains=search), q_search.OR)
                q_search.add(Q(contents__contains=search), q_search.OR)
                q.add(q_search, q.AND)

            if hashtag:
                q_hashtag = Q()
                for h in hashtag.replce('#', '').split(','):
                    q_hashtag.add(Q(hashtag__hashtag_name=h), q_hashtag.OR)
                q.add(q_hashtag, q.AND)

                subquery = (
                    self.queryset.filter(q)
                    .values('id')
                    .annotate(count=Count('id'))
                    .filter(count__gte=len(hashtag))
                    .values('id')
                )
                queryset = self.queryset.filter(id__in=subquery).order_by(ordering)[offset:limite]
            else:
                queryset = self.queryset.filter(q).order_by(ordering)[offset:limite]

            serializer = PostSearchSerializer(queryset, many=True)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        except Exception as ex:
            print(ex)
            raise APIException(detail='error occurred', code=ex)

    # TODO: nginx 적용 후 IP 구별 후 과도한 조회수 증가 금지 로직 구현
    @transaction.atomic
    def retrieve(self, request, *args, **kwargs):

        user_ip = get_client_ip(request)
        post_obj = self.queryset.filter(id=kwargs.get('post_id')).first()

        if not post_obj:
            return Response({'detail': 'not existed post'}, status=status.HTTP_404_NOT_FOUND)

        try:
            cache_data = cache.get(str(user_ip))
            print(cache_data)
            if not cache_data:
                cache.set(str(user_ip), 'true', 300)

                post_obj.hits += 1
                post_obj.save()

            # post_obj.hits += 1
            # post_obj.save()

            serializer = PostDetailSearchSerializer(post_obj)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        except Exception as ex:
            print(ex)
            raise APIException(detail='error occurred', code=ex)


class PostLikeViewSet(viewsets.ModelViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user = request.user
        post_id = kwargs['post_id']

        try:
            post_obj = Post.objects.filter(id=post_id).first()
            post_like_obj = self.queryset.filter(user=user, post=post_obj)

            if post_like_obj:
                post_like_obj.delete()
            else:
                serializer = PostLikeSerializer(data={'user': user.id, 'post': post_obj.id})
                serializer.is_valid(raise_exception=True)
                serializer.save()

            return Response({'detail': 'sucess, accepted'}, status=status.HTTP_202_ACCEPTED)

        except Exception as ex:
            print(ex)
            raise APIException(detail='error occurred', code=ex)
