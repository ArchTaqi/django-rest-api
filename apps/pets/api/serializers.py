from rest_framework import serializers
from django.conf import settings
from ..models import *

User = settings.AUTH_USER_MODEL


class HelloWorldSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=6)
    age = serializers.IntegerField(required=False, min_value=10, default=10)


class PetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PetCategory
        fields =  '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("name", "zip_code")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class PetSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=160)
    description = serializers.CharField()
    contact_number = serializers.CharField(max_length=15)
    owner = serializers.StringRelatedField(many=False)
    # owner = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Pet
        fields = [
            'id',
            'name',
            'description',
            'contact_number',
            'category',
            'tags',
            'photoUrls',
            'status',
            'owner'
        ]
        extra_kwargs = {'owner': {'read_only': True}}


class UserProfileSerializer(serializers.ModelSerializer):
    """A serializer for our user objects."""

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Create and return a new user."""

        user = User(
            email=validated_data['email'],
            name=validated_data['name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user