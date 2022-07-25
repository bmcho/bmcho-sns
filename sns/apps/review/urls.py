from django.urls import path

from .views import ReviewViewset

review_view = ReviewViewset.as_view({'post': 'create', 'patch': 'partial_update'})


urlpatterns = [
    path('', review_view, name='review_view'),
]
