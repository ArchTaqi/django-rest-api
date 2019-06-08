from django.urls import path, re_path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from .views import UserViewSet, CreateUserView, ActivateUser

router = DefaultRouter(trailing_slash=False)
router.register('users', UserViewSet, base_name='users')


urlpatterns = [
    # rest of url patterns
    re_path('^api/(?P<version>(v1|v2))/', include(router.urls)),
    path('api-auth/', obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
    path('api-register/', CreateUserView.as_view()),
    path(
        'api-activate/(?P<token>.+?)/',
        ActivateUser.as_view(),
        name='activate-user'
    ),

    # path('auth/login/', LoginView.as_view(), name="auth-login"),
    # path('auth/register/', RegisterUsers.as_view(), name="auth-register"),
]