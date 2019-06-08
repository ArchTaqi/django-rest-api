# from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
#
# from apps.likes import LikedMixin
# from ..models import Tweet
# from .serializers import TweetSerializer
#
#
# class TweetViewSet(LikedMixin,
#                    viewsets.ModelViewSet):
#     queryset = Tweet.objects.all()
#     serializer_class = TweetSerializer
#     permission_classes = (IsAuthenticatedOrReadOnly, )
