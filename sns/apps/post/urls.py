from django.urls import path

from .views import PostViewSet

post_serach_create = PostViewSet.as_view({'post': 'create', 'get': 'list'})
post_detail_modify = PostViewSet.as_view({'patch': 'partial_update', 'get':'retrieve'})

urlpatterns = [
    path('', post_serach_create, name='post_serach_create'),
    path('/<int:post_id>', post_detail_modify, name='post_detail_modify'),
]
