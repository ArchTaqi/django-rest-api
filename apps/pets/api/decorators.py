import jwt
from rest_framework.response import Response
from rest_framework.views import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions

from django.conf import settings
User = settings.AUTH_USER_MODEL


def validate_request_data(fn):
    def decorated(*args, **kwargs):
        # args[0] == GenericView Object
        title = args[0].request.data.get("name", "")
        artist = args[0].request.data.get("zip_code", "")
        if not title and not artist:
            return Response(
                data={
                    "message": "Both name and zip code are required to add a city"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)
    return decorated


class IsSeller(permissions.BasePermission):
    message = 'You are not a owner'

    def has_permission(self, request, view):
        try:
            if request.user.is_staff:
                return True
            seller = User.objects.get(id=request.user.id)
            request.user.__dict__['seller'] = seller
        except ObjectDoesNotExist:
            return False
        else:
            return True


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            if request.user.is_staff:
                return True
            owner = User.objects.get(id=request.user.id)
            request.user.__dict__['owner'] = owner
        except ObjectDoesNotExist:
            return False
        else:
            return True


class IsTokenAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            encoded_jwt = request.META.get('Authorization', request.META.get('HTTP_AUTHORIZATION', '')).split(' ')[-1]
            decoded_jwt = jwt.decode(encoded_jwt, key=settings.SECRET_KEY, leeway=30, algorithms=['HS256'])
            user_id = decoded_jwt.get('user_id')
            user = User.objects.get(id=user_id)
            request.user = user
            request.user.__dict__['is_authenticated'] = True
        except jwt.ExpiredSignature:
            return False
        except ObjectDoesNotExist:
            return False
        else:
            return True