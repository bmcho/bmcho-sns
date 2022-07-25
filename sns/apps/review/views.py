from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.post.models import Post
from apps.review.models import Review
from apps.review.serializers import (
    ReivewCreateCheckSerializers,
    ReivewDeleteCheckSerializers,
    ReivewUpdateCheckSerializers,
    ReviewSerializers,
)


# Create your views here.
class ReviewViewset(viewsets.ModelViewSet):
    """Review CRUD ViewSet

    Wirter:조병민
    Data: 2022-07-25

    """

    queryset = Review.objects.order_by('-created_at').all()
    serializer_class = ReviewSerializers
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        check_serializer = ReivewCreateCheckSerializers(data=request.data)
        check_serializer.is_valid(raise_exception=True)

        try:
            user_id = request.user.id
            post_id = kwargs['post_id']
            review = request.data['review']

            if not Post.objects.filter(id=post_id).first():
                return Response({'detail': 'not existed post'}, status=status.HTTP_404_NOT_FOUND)

            serializer = ReviewSerializers(data={'user_id': user_id, 'post_id': post_id, 'review': review})
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({'detail': 'sucess, review created'}, status=status.HTTP_201_CREATED)

        except Exception as ex:
            print(ex)
            raise APIException(detail='error occurred', code=ex)

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        check_serializer = ReivewUpdateCheckSerializers(data=request.data)
        check_serializer.is_valid(raise_exception=True)

        try:
            user_id = request.user.id
            review_id = request.data['review_id']
            review = request.data['review']

            review_obj = self.queryset.filter(id=review_id).first()

            if not review_obj:
                return Response({'detail': 'not existed reivew'}, status=status.HTTP_404_NOT_FOUND)

            review_obj = self.queryset.filter(id=review_id, user_id=user_id).first()

            if not review_obj:
                return Response({'detail': 'not the author'}, status=status.HTTP_401_UNAUTHORIZED)

            serializer = ReviewSerializers(review_obj, data={'review': review}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({'detail': 'sucess, accepted'}, status=status.HTTP_202_ACCEPTED)

        except Exception as ex:
            print(ex)
            raise APIException(detail='error occurred', code=ex)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        check_serializer = ReivewDeleteCheckSerializers(data=request.data)
        check_serializer.is_valid(raise_exception=True)

        try:
            user_id = request.user.id
            review_id = request.data['review_id']

            review_obj = self.queryset.filter(id=review_id).first()

            if not review_obj:
                return Response({'detail': 'not existed reivew'}, status=status.HTTP_404_NOT_FOUND)

            review_obj = self.queryset.filter(id=review_id, user_id=user_id).first()

            if not review_obj:
                return Response({'detail': 'not the author'}, status=status.HTTP_401_UNAUTHORIZED)

            review_obj.delete()

        except Exception as ex:
            print(ex)
            raise APIException(detail='error occurred', code=ex)
