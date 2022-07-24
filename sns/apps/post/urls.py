from django.urls import path

from .views import PostViewSet

post_list = PostViewSet.as_view({'post': 'create'})


urlpatterns = [
    path('', post_list, name='post-list'),
]
