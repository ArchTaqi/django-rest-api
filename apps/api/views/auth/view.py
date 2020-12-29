# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


class Auth(views.APIView):

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response(
                {
                    'username, password': [
                        'This fields are required.'
                    ]
                },
                status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                {
                    'detail': [
                        'Invalid Credentials'
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                'token': token.key
            },
            status=status.HTTP_200_OK
        )
