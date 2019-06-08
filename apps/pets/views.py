# from django.shortcuts import get_object_or_404
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework import status, permissions
# from rest_framework.exceptions import PermissionDenied
# from django.http import HttpResponse, JsonResponse
# from django.core.paginator import Paginator
# from django.contrib.auth.decorators import permission_required
# from .serializer import PetSerializer
# from .models import Pet
# # Create your views here.
#

#
#
# # from rest_framework.views import APIView
# # from rest_framework.parsers import MultiPartParser, FormParser
# # from rest_framework.response import Response
# # from rest_framework import status
# # from apps.petstore.models import *
# # from apps.petstore.serializer import PetSerializer
# #
# #
# # class IndexPetView(APIView):
# #     # MultiPartParser AND FormParser
# #     # https://www.django-rest-framework.org/api-guide/parsers/#multipartparser
# #     # "You will typically want to use both FormParser and MultiPartParser
# #     # together in order to fully support HTML form data."
# #     parser_classes = (MultiPartParser, FormParser)
# #
# #     def post(self, request, *args, **kwargs):
# #         file_serializer = PetSerializer(data=request.data)
# #         if file_serializer.is_valid():
# #             file_serializer.save()
# #             return Response(file_serializer.data, status=status.HTTP_201_CREATED)
# #         else:
# #             return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# # from django.shortcuts import render
# # from django.views import generic
# # from django.contrib.auth.mixins import LoginRequiredMixin
# # from apps.petstore.models import *
# # # Create your views here.
# #
# #
# #
# # def getPetById(petId):
# #     """
# #     Find pet by ID, Returns a pet when ID < 10. " + "ID > 10 or nonintegers will simulate API error conditions
# #     ApiErrors
# #         - 400, reason = "Invalid ID supplied"
# #         - code = 404, reason = "Pet not found"
# #     :param petId: required = true, ID of pet that needs to be fetched
# #     :return:
# #     """
# #     print('Hello')
# #
# #
# # def addPet(pet):
# #     """
# #     Add a new pet to the store
# #     API Errors
# #         - 405, Invalid input
# #     :param pet: required = true, Pet object that needs to be added to the store
# #     :return:
# #     """
# #     print('Hello')
# #
# #
# # def updatePet(pet):
# #     """
# #     Update an existing pet
# #     400 - Invalid ID supplied
# #     404 - pet not found
# #     405 - Validation exception
# #     :param pet: required = true, Pet object that needs to be added to the store
# #     :return:
# #     """
# #     print('Hello')
# #
# #
# #
# # def findPetsByStatus(status):
# #     """
# #     Finds Pets by status, Multiple status values can be provided with comma separated strings.
# #     Invalid status value if 400
# #     status - Status values that need to be considered for filter
# #     :param status: status  required=true, defaultValue="available", allowableValues="available,pending,sold", allowMultiple=true
# #     :return:
# #     """
# #     print('Hello')
# #
# #
# # def findPetsByTags(tags):
# #     """
# #     "Finds Pets by tags, Multiple tags can be provided with comma separated strings. Use tag1, tag2, tag3 for testing."
# #     :param tags: tags String value = "Tags to filter by", required = true, allowMultiple = true
# #     :return:
# #     """
# #     print('Hello')
# #
# #
# # #
# # # class Index(LoginRequiredMixin, generic.View):
# # #     template_name = "index.html"
# # #     login_url = 'login/'
# # #
# # #     def __init__(self, **kwargs):
# # #         pass
# # #
# # #     def get(self, request):
# # #         if request.user.is_superuser:
# # #             organizations = Pet.objects.filter(owner=request.user)
# # #         else:
# # #             organizations = Pet.objects.filter()
# # #
# # #         return render(request, self.template_name, {'organizations': organizations})
# # #
# # #
# # # class OrganizationProfile(LoginRequiredMixin, generic.DetailView):
# # #     template_name = "profile.html"
# # #     login_url = 'login/'
# # #
# # #     def __init__(self, **kwargs):
# # #         pass
# # #
# # #     def get(self, request, petId, *args, **kwargs):
# # #         organization = Pet.objects.get(pk=petId)
# # #
# # #         if request.user.is_superuser:
# # #             organization = Pet.objects.get(pk=petId)
# # #
# # #         return render(request, self.template_name, {'organization': organization})
# # #
# # #
# # # class Browse(LoginRequiredMixin, generic.View):
# # #     template_name = "browse.html"
# # #     login_url = 'login/'
# # #
# # #     def __init__(self, **kwargs):
# # #         pass
# # #
# # #     def get(self, request):
# # #         categories = Category.objects.filter(active=True).order_by('name')
# # #         cities = City.objects.filter(active=True).order_by('name')
# # #         return render(request, self.template_name, {'categories': categories, 'cities': cities})
#
#
# # from apps.petstore.models import Pet
# # from apps.petstore.serializer import *
# # from apps.petstore.permissions import ReadOnly
# # from rest_framework.response import Response
# # from django.http import Http404
# # # Create your views here.
# #

# # ################################# Function Based APIView ###############################################################
# #
# #
# # from rest_framework.views import APIView
# # from apps.petstore.serializer import HelloWorldSerializer
# #
# #
# # # class HelloWorldView(APIView):
# # #     def get(self, request):
# # #         return Response({"message": "Hello World!"})
# # #
# # #     def post(self, request):
# # #         serializer = HelloWorldSerializer(data=request.data)
# # #         if serializer.is_valid():
# # #             valid_data = serializer.data # Cleaning same as we do in Django Forms
# # #
# # #             name = valid_data.get("name")
# # #             age = valid_data.get("age")
# # #
# # #             return Response({"message": "Hello {}, you're {} years old".format(name, age)}, status=status.HTTP_201_CREATED)
# # #         else:
# # #             return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
# #
# #
# # class RESTPetView(APIView):
# #
# #     def get_object(self, pk):
# #         try:
# #             return Pet.objects.get(pk=pk)
# #         except Pet.DoesNotExist:
# #             raise Http404
# #
# #     def get(self, request):
# #         all_pets = Pet.objects.filter(status='available').all()
# #         serialized_pets = PetSerializer(all_pets, many=True)
# #         return Response(serialized_pets.data)
# #
# #     # def get(self, request, pk, format=None):
# #     #     product = self.get_object(pk)
# #     #     serializer = PetSerializer(product)
# #     #     return Response(serializer.data)
# #
# #     def post(self, request):
# #         serializer = PetSerializer(data=request.data)
# #         if serializer.is_valid():
# #             subscriber_instance = Pet.objects.create(**serializer.data)
# #             return Response({"message": "Created Pet {}".format(subscriber_instance.id)})
# #         else:
# #             return Response({"errors": serializer.errors})
# #
# #     def put(self, request, pk, format=None):
# #         product = self.get_object(pk)
# #         serializer = PetSerializer(product, data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #
# #     def delete(self, request, pk, format=None):
# #         product = self.get_object(pk)
# #         product.delete()
# #         return Response(status=status.HTTP_204_NO_CONTENT)
# # #
# # # ################################# DRF: ViewSet, ModelViewSet and Router #################################
# # #
# # #
# # # from rest_framework import viewsets, permissions, status
# # #
# # #
# # # # class UserViewSet(viewsets.ModelViewSet):
# # # #     """
# # # #     Provides basic CRUD functions for the User model
# # # #     """
# # # #     queryset = User.objects.all()
# # # #     serializer_class = UserSerializer
# # # #     permission_classes = (ReadOnly, )
# # #
# # #
# # # class PetViewSet(viewsets.ModelViewSet):
# # #     """
# # #     Provides basic CRUD functions for the Pet model
# # #     retrieve:
# # #         Return a user instance.
# # #
# # #     list:
# # #         Return all users, ordered by most recently joined.
# # #
# # #     create:
# # #         Create a new user.
# # #
# # #     delete:
# # #         Remove an existing user.
# # #
# # #     partial_update:
# # #         Update one or more fields on an existing user.
# # #
# # #     update:
# # #         Update a user.
# # #     """
# # #     queryset = Pet.objects.all()
# # #     serializer_class = PetSerializer
# # #     # permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
# # #     # permission_classes = (permissions.IsAuthenticated,)
# # #
# # #     def perform_create(self, serializer):
# # #         serializer.save(user=self.request.user)
# # #
# # #
# # # class PetViewSet(viewsets.ModelViewSet):
# # #     """
# # #     Provides basic CRUD functions for the Pet model
# # #     retrieve:
# # #         Return a user instance.
# # #
# # #     list:
# # #         Return all users, ordered by most recently joined.
# # #
# # #     create:
# # #         Create a new user.
# # #
# # #     delete:
# # #         Remove an existing user.
# # #
# # #     partial_update:
# # #         Update one or more fields on an existing user.
# # #
# # #     update:
# # #         Update a user.
# # #     """
# # #     queryset = Pet.objects.all()
# # #     serializer_class = PetSerializer
# # #     # permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
# # #     # permission_classes = (permissions.IsAuthenticated,)
# # #
# # #     def perform_create(self, serializer):
# # #         serializer.save(user=self.request.user)
# # #
# # #
# # # class findByStatusView(APIView):
# # #     """
# # #     summary: "Finds Pets by status"
# # #     description: "Multiple status values can be provided with comma seperated strings"
# # #     operationId: "findPetsByStatus"
# # #     parameters:
# # #       - name: "status"
# # #         description: "Status values that need to be considered for filter"
# # #         required: true
# # #         type: "array"
# # #         items:
# # #           type: "string"
# # #           enum:
# # #           - "available"
# # #           - "pending"
# # #           - "sold"
# # #           default: "available"
# # #     """
# # #
# # #     def get(self, request):
# # #         all_hashtags = Pet.objects.all()
# # #         serialized_hashtags = PetSerializer(all_hashtags, many=True)
# # #         return Response(serialized_hashtags.data)