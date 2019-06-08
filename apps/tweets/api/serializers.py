# from rest_framework import serializers
#
# from apps.likes import services as likes_services
# from ..models import Tweet
#
#
# class TweetSerializer(serializers.ModelSerializer):
#     is_fan = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Tweet
#         fields = (
#             'id',
#             'body',
#             'is_fan',
#             'total_likes',
#         )
#
#     def get_is_fan(self, obj) -> bool:
#         """Check if a `request.user` has liked this tweet (`obj`).
#         """
#         user = self.context.get('request').user
#         return likes_services.is_fan(obj, user)
