from django.urls import path, re_path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from .api import viewsets

router = DefaultRouter(trailing_slash=False)
router.register("cities", viewsets.CityViewSet, base_name='city')
router.register("pets", viewsets.RESTPetViewSet, base_name='pets')
router.register("pets-pets", viewsets.RESTPetModelViewSet, base_name='pets')
# router.register("users", viewsets.UserViewSet, base_name='users')

urlpatterns = [
    path('ping', viewsets.ping, name="ping"),
    path('category/<int:category_id>/', viewsets.get_category),
    path('category/list/', viewsets.list_category),
    path('category/create/', viewsets.create_category),

    path('city/', viewsets.ListCreateCityView.as_view(), name="cities-list-create"),
    path('city/<int:pk>/', viewsets.CityDetailView.as_view(), name="cities-detail"),
    path('api/v1/pets', viewsets.RESTPetAPIView.as_view(), name="pets"),
    # path(r'hash-tags/v2', PetViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name="hashtags_v2"),

    re_path('^api/(?P<version>(v1|v2))/', include(router.urls)),
]