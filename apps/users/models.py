from django.contrib.auth.models import AbstractUser
from rest_framework import serializers
from ..pets.models import Pet


class User(AbstractUser):
    pass


class UserSerializer(serializers.ModelSerializer):
    pets = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Pet.objects.all()
    )

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'pets'
        ]

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()
        return user
