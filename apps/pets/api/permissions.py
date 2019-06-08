from rest_framework import permissions

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class ReadOnly(permissions.BasePermission):
    """
    The endpoint is read-only request.
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
    )


class UpdateOwnProfile(permissions.BasePermission):
    """Allow users to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile"""

        # GET is in SAFE_METHODS, not PUT< POST.
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id

