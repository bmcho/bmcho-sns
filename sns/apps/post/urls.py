from django.urls import path

from .views import PostLikeViewSet, PostViewSet

post_serach_create = PostViewSet.as_view({'post': 'create', 'get': 'list'})
post_detail_modify = PostViewSet.as_view({'patch': 'partial_update', 'get': 'retrieve', 'delete': 'destroy'})
post_like = PostLikeViewSet.as_view({'post': 'create'})

urlpatterns = [
    path('', post_serach_create, name='post_serach_create'),
    path('/<int:post_id>', post_detail_modify, name='post_detail_modify'),
    path('/<int:post_id>/like', post_like, name='post_like'),
]
