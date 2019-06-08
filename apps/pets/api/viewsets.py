import os, datetime, time
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView, status
from rest_framework.viewsets import ViewSet, GenericViewSet, ModelViewSet
from rest_framework.decorators import api_view, permission_classes, list_route, detail_route
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404
from django.core.paginator import Paginator
from django.conf import settings

from apps.pets.api.decorators import validate_request_data, IsSeller, IsOwner
from ..models import City, PetCategory, Pet
from .serializers import CitySerializer, PetCategorySerializer, PetSerializer

User = settings.AUTH_USER_MODEL

########################################################################################################################
# USING decorators and Functions
########################################################################################################################


@api_view(["GET", "POST"])
@permission_classes((permissions.AllowAny,))
def ping(request):
    if request.method == "GET":
        return Response({"message": "Pong!"})
    else:
        name = request.data.get("name")
        if not name:
            return Response({"error": "No name passed"})
        return Response({"message": "Pong {}!".format(name)})


@api_view(['GET'])
@permission_classes((permissions.AllowAny, ))
def get_category(request, category_id):
    category = get_object_or_404(PetCategory, id=category_id)
    category_json = PetCategorySerializer(category)
    return Response(category_json.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsSeller & permissions.IsAdminUser, ))
def list_category(request):
    categories_list = PetCategory.objects.all()
    paginator = Paginator(categories_list, 20)
    page = request.GET.get('page')
    clinics = paginator.get_page(page)
    page_json = PetCategorySerializer(clinics, many=True)
    return JsonResponse(
        page_json.data,
        safe=False,
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes((IsSeller & IsOwner, ))
def create_category(request):
    PetCategory.objects.create(
        name=request.data['name'],
        description=request.data['description'],
        active=request.data['active'],
    )
    return Response(PetCategory, status=status.HTTP_200_OK)

########################################################################################################################
# APIViews
########################################################################################################################


class RESTPetAPIView(APIView):
    """
    def get(self, request, format=None)
    def post(self, request):
    def put(self, request, pk=None):
    def patch(self, request, pk=None):
    def delete(self, request, pk=None):
    """
    serializer_class = PetSerializer

    def get_object(self, pk):
        try:
            return Pet.objects.get(pk=pk)
        except Pet.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        all_pets = Pet.objects.filter(status='1').all()
        serialized_pets = self.serializer_class(all_pets, many=True)
        return Response(serialized_pets.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            subscriber_instance = Pet.objects.create(**serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            # return Response({"message": "Created Pet {}".format(subscriber_instance.id)})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = self.serializer_class(product, data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

########################################################################################################################
# ViewSet
########################################################################################################################


class RESTPetViewSet(ViewSet):
    """Test API ViewSet.
    def list(self, request)
    def create(self, request)
    def retrieve(self, request, pk=None)
    def update(self, request, pk=None)
    def partial_update(self, request, pk=None)
    def destroy(self, request, pk=None)
    """

    serializer_class = PetSerializer

    def get_object(self, pk):
        try:
            return Pet.objects.get(pk=pk)
        except Pet.DoesNotExist:
            raise Http404

    def list(self, request):
        """Return all pets"""

        all_pets = Pet.objects.filter(status='1').all()
        serialized_pets = self.serializer_class(all_pets, many=True)
        return Response(serialized_pets.data)

    def create(self, request):
        """Create a new Pet."""

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            subscriber_instance = Pet.objects.create(**serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handles getting an object by its ID."""
        pet = self.get_object(pk)
        serializer = PetSerializer(pet)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handles updating an object."""
        pet = self.get_object(pk)
        serializer = self.serializer_class(pet, data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        """Handles updating part of an object."""

        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """Handle removing an object"""
        pet = self.get_object(pk)
        pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RESTPetModelViewSet(ModelViewSet):
    """
    Provides basic CRUD functions for the Pet model
    def list(self, request)
    def create(self, request)
    def retrieve(self, request, pk=None)
    def update(self, request, pk=None)
    def partial_update(self, request, pk=None)
    def destroy(self, request, pk=None)
    """
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    ordering = ('-created_at',)
    search_fields = ('name', )

    def perform_create(self, serializer):
        """
        this method is called on every serializer.save before
        :param serializer:
        :return:
        """
        serializer.save(user=self.request.user)

    upload_file_path = settings.UPLOAD_FILE_PATH

    @list_route(methods=["POST"])
    def upload(self, request, *args, **kwargs):
        """上传文件"""
        file_obj = request.FILES.get('photoUrls', None)
        filename = file_obj.name
        filename = '{}{}'.format(int(time.time()*10**7), filename)
        try:
            with open(self.upload_file_path + filename, 'wb') as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)
        except Exception as e:
            return Response({'message': '%s' % e}, status.HTTP_400_BAD_REQUEST)
        else:
            Pet.objects.create(
                file_name=filename,
                file_path=self.upload_file_path + filename
            )
            return Response({'message': 'OK'}, status.HTTP_200_OK)

# class UserViewSet(ModelViewSet):
#     """
#     Provides basic CRUD functions for the User model
#     """
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = (ReadOnly, UpdateOwnProfile)
#     authentication_classes = (TokenAuthentication, )
#     filter_backends = (filters.SearchFilter,)
#     search_fields = ('name', 'email',)


########################################################################################################################
# Generic Views
########################################################################################################################


class PetViewListCreate(generics.ListAPIView, generics.CreateAPIView):
    serializer_class = PetSerializer
    queryset = Pet.objects.all()


class PetViewCreate(generics.ListCreateAPIView):
    serializer_class = PetSerializer
    queryset = Pet.objects.all()

################################# DRF: ViewSet, ModelViewSet and Router #################################


class findByStatusView(APIView):
    """
    summary: "Finds Pets by status"
    description: "Multiple status values can be provided with comma seperated strings"
    operationId: "findPetsByStatus"
    parameters:
      - name: "status"
        description: "Status values that need to be considered for filter"
        required: true
        type: "array"
        items:
          type: "string"
          enum:
          - "available"
          - "pending"
          - "sold"
          default: "available"
    """

    def get(self, request):
        all_hashtags = Pet.objects.all()
        serialized_hashtags = PetSerializer(all_hashtags, many=True)
        return Response(serialized_hashtags.data)




class ListCreateCityView(generics.ListCreateAPIView):
    """
    GET cities/
    POST cities/
    """
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = (permissions.IsAuthenticated,)

    @validate_request_data
    def post(self, request, *args, **kwargs):
        a_song = City.objects.create(
            name=request.data["name"],
            zip_code=request.data["zip_code"]
        )
        return Response(
            data=CitySerializer(a_song).data,
            status=status.HTTP_201_CREATED
        )


class CityDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET city/:id/
    PUT city/:id/
    DELETE city/:id/
    """
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def get(self, request, *args, **kwargs):
        try:
            a_song = self.queryset.get(pk=kwargs["pk"])
            return Response(CitySerializer(a_song).data)
        except City.DoesNotExist:
            return Response(
                data={
                    "message": "City with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_request_data
    def put(self, request, *args, **kwargs):
        try:
            a_song = self.queryset.get(pk=kwargs["pk"])
            serializer = CitySerializer()
            updated_song = serializer.update(a_song, request.data)
            return Response(CitySerializer(updated_song).data)
        except City.DoesNotExist:
            return Response(
                data={
                    "message": "City with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_song = self.queryset.get(pk=kwargs["pk"])
            a_song.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except City.DoesNotExist:
            return Response(
                data={
                    "message": "City with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class CityViewSet(GenericViewSet,  # generic view functionality
                     CreateModelMixin,  # handles POSTs
                     RetrieveModelMixin,  # handles GETs for 1 Company
                     UpdateModelMixin,  # handles PUTs and PATCHes
                     ListModelMixin):  # handles GETs for many Companies

    serializer_class = CitySerializer
    queryset = City.objects.all()

