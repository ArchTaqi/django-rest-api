## JWT Authentication in Django Rest Framework

### JWT versus API key

API key is usually generated and that’s it! It usually doesn’t expire unless such mechanism is implemented on server side. By using API key, each request to server will include a header with the key. API key creates security issue if such key are exposed to unauthorized user (i.e: captured in man-in-the-middle attack). It could be used by unauthorized party to perform legit request.
Unlike API token, JWT has an expiry timestamp, it has to be constantly renewed or refreshed to keep the token valid. If such token is exposed to third party, he/she might not be able to refresh the token and it will be invalidated after it’s expiring timestamp.

### JWT versus Cookie-based sessions

To keep track of all user sessions, server has to maintain a record of those. In Django, user sessions are stored and maintained in it’s underlying DB. This constraints scalability of the system, even if system are distributed and scaled horizontally, each node will still have to retrieve the session data stored in underlying database. Second, it is even more complex to make your session universal across multiple domains.
JWT can save you a lot of fuss when dealing with authentication across multiple domain and horizontal scalability since there is no need to keep session stored.

### Set up DRF with JWT

`pipenv install djangorestframework_jwt`

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
}
JWT_AUTH = {
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(hours=1),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',  # Bearer <token>
    'JWT_SECRET_KEY': SECRET_KEY or "235856!gsdgsd",
}
```

```python
# urls.py
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
  ...
  url(r'^auth/obtain_token/', obtain_jwt_token),
  url(r'^auth/refresh_token/', refresh_jwt_token),
  ...
]
```
**GET JWT Token**
`$ curl -X POST -H "Content-Type: application/json" -d '{"username":"<your_username>","password":"<your_password>"}' http://<your_domain_and_port>/auth/obtain_token`

**REFRESH Token**
`$ curl -X POST -H "Content-Type: application/json" -d '{"token":"<EXISTING_TOKEN>"}' http://<your_domain_and_port>/auth/refresh_token/`

**Consume Endpoint**
`$ http POST 127.0.0.1:8000/api/customers/ 'Authorization: Bearer <jwt-token>'`


## Consume Your REST Service from Vue.js

`npm install --save vue-axios axios vuex jwt-decode`

Todo : https://melvinkoh.me/jwt-authentication-in-vuejs-and-django-rest-framework-part-2-cjye5a3ss001qvvs1fi123163



# JSON Web Token in Python

> The traditional mode of authentication for websites has been to use cookie based authentication.
In a typical REST architecture the server does not keep any client state. The stateless approach of REST makes session cookies inappropriate from the security standpoint.
Session hijacking and cross-site request forgery are common security issues while using cookies to secure your REST Service.
Hence their arises a need to authenticate and secure a stateless REST service.

#### Working of JWT

- When using JWT for authentication you'd usually store the token in the browser's localstorage or sessionstorage. To logout you just remove the token. There's nothing else to invalidate. 
- One of the benefits of using this kind of approach for authentication is that tokens are not persisted in the database, so you don't have to query a session store for anything when authenticating.

Lets take a look at it with the help of this simple illustration -

![image][2]

#### Structure of a JWT

JSON Web Token example:

    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ0b3B0YWwuY29tI iwiZXhwIjoxNDI2NDIwODAwLCJodHRwOi8vdG9wdGFsLmNvbS9qd3RfY2xhaW1zL2lzX2FkbWluI jp0cnVlLCJjb21wYW55IjoiVG9wdGFsIiwiYXdlc29tZSI6dHJ1ZX0.yRQYnWzskCZUxPwaQupWk iUzKELZ49eM7oWxAQK_ZXw

Since there are 3 parts separated by a ., each section is created differently, which are:

<base64-encoded header="">.<base64-encoded payload="">.<base64-encoded signature="">

##### **Header**

The JWT Header declares that the encoded object is a JSON Web Token (JWT) and the JWT is a JWS that is MACed using the HMAC SHA-256 algorithm. For example:

    {
        "alg": "HS256",
        "typ": "JWT"
    }

- "alg" specifies the algorithm used to sign the token.
- "typ" specifies that this is a JWT token.

##### **Payload (Claims)**

A claim or a payload can be defined as a statement about an entity that contians security information as well as additional meta data about the token itself.

Following are the claim attributes :

* iss: The issuer of the token
* sub: The subject of the token
* aud: The audience of the token
* qsh: query string hash
* exp: Token expiration time defined in Unix time
* nbf: "Not before" time that identifies the time before which the JWT must not be accepted for processing
* iat: "Issued at" time, in Unix time, at which the token was issued
* jti: JWT ID claim provides a unique identifier for the JWT

##### **Signature**

Signature

JSON Web Signatre specification are followed to generate the final signed token.
JWT Header, the encoded claim are combined, and an encryption algorithm, such as HMAC SHA-256 is applied.
The signatures's secret key is held by the server so it will be able to verify existing tokens.

#### Popular Libraries for JWT

#### Advantages of Token Based Approach

* JWT approach allows us to make AJAX calls to any server or domain. Since the HTTP header is used to transmit the user information.
* Their is no need for having a separate session store on the server. JWT itself conveys the entire information.
* Server Side reduces to just an API and static assets(HTML, CSS, JS) can be served via a CDN.
* The authentication system is mobile ready, the token can be generated on any device.
* Since we have eliminated the need for cookies, we no more need to protect against the cross site requesets.
* API Keys provide either-or solution, whereas JWT provide much granular control, which can be inspected for any debugging purpose.
* API Keys depend on a central storage and a service. JWT can be self-issued or an external service can issue it with allowed scopes and expiration.

#### Creating a JWT in Python

Encoding a payload

    &gt;&gt;&gt; import jwt
    &gt;&gt;&gt; encoded = jwt.encode({'some': 'payload'}, 'secret', algorithm='HS256')
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9.4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg'

Decoding a payload on the server

    &gt;&gt;&gt; jwt.decode(encoded, 'secret', algorithms=['HS256'])
    {'some': 'payload'}
    
  </base64-encoded></base64-encoded></base64-encoded>

## How can you use JWT and why?
When you get your response back from a server with JSON Web Token you can use it in header like this:

    Authorization: Bearer <JWT token>

JSON Web Token looks like this:

    HEADER.PAYLOAD.SIGNATURE

## Setting Up Basic App

Task Model

    from django.db import models
    from django.contrib.auth.models import User

    class Task(models.Model):
        title = models.CharField(max_length=100)
        person = models.ForeignKey(User)
        due_to = models.DateTimeField()

        def __str__(self):
            return 'Task with title: {}'.format(self.title)

and create serializers so data from database can be converted to stream of bytes:

    from rest_framework import serializers
    from .models import Task
    from django.contrib.auth.models import User

    class TaskSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = Task

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User


TaskSerializer used HyperlinkedModelSerializer (a type of serializer) - so that response from my application will have hyperlinks to resources instead of just primary keys.

create some views and urls.
For a typical usage of views, DRF gives you generic viewsets like ModelViewSet.
ViewSet is a combination of the logic for a set of related views in a single class. How do views look like?

    from rest_framework import viewsets
    from .models import Task
    from .serializers import TaskSerializer, UserSerializer
    from django.contrib.auth.models import User

    class TaskViewSet(viewsets.ModelViewSet):
        # ModelViewSet needs minimum queryset and serializer_class arguments so viewsets know which data they needed to take and which serializer use.
        queryset = Task.objects.all()
        serializer_class = TaskSerializer

    class UserViewSet(viewsets.ModelViewSet):
        queryset = User.objects.all()
        serializer_class = UserSerializer

urls:

    from django.conf.urls import url, include
    from django.contrib import admin
    from tasks import views
    from rest_framework.routers import DefaultRouter

    router = DefaultRouter()
    router.register(r'tasks', views.TaskViewSet)
    router.register(r'users', views.UserViewSet)

    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^', include(router.urls)),
    ]


$ http GET 127.0.0.1:8000
$ http GET 127.0.0.1:8000/tasks/

#### Implementing JWT in DRF application

    class Task(models.Model):
        # rest of model
        person = models.ForeignKey('auth.User', related_name='tasks')

It is the same model definition but written using string. The code in Django responsible for model lookup based on the string can be seen ![here][1].

Then I added an additional field to UserSerializer- thanks to that when getting info about the user I also get info about which tasks this user has. It can be accomplished by:

    class UserSerializer(serializers.ModelSerializer):
        tasks = serializers.PrimaryKeyRelatedField(
            many=True, queryset=Task.objects.all()
        )

        # rest of the code


As I got my models and serializers ready I need views:

    from rest_framework import permissions


    class TaskViewSet(viewsets.ModelViewSet):
        # rest of the code

        permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


    class UserViewSet(viewsets.ModelViewSet):
        # rest of the code

        permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

I added permission_classes to tell DRF that these views are read only when the user is not authenticated. If I send a token ( or authenticate in another way) I am able to modify data kept under this view. To authenticate I needed a new endpoint so there's a small change to urls.py:

from rest_framework_jwt.views import obtain_jwt_token

    urlpatterns = [
        # rest of the code
        url(r'^api-auth/', obtain_jwt_token),
    ]

Right now the user firsts need to authenticate using this endpoint. In return, endpoint gives back a token. Last thing to let this work is to tell Django Rest Framework that I want to use JWT as a basic type of authentication in settings.py:

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        )
    }

$ http GET 127.0.0.1:8000/tasks/
$ cat create_task.json
    {
      "due_to": "2016-10-18T19:12:01Z",
      "person": 1,
      "title": "Next one",
    }

$ http POST 127.0.0.1:8000/tasks/ < create_task.json

    {
        "detail": "Authentication credentials were not provided."
    }

$ http POST 127.0.0.1:8000/api-auth/ username=admin password=admin

    {
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE0Nzc4MTc4NTMsImVtYWlsIjoiYWRtaW5AZXhhbXBsZS5jb20iLCJ1c2VybmFtZSI6ImFkbWluIiwidXNlcl9pZCI6MX0.xWlhwgzzVjDwgTPp48AgAYDJnraGThlkGmBnJbKnA74"
    }

$ http POST 127.0.0.1:8000/tasks/ < create_task.json 'Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE0Nzc4MTc4NTMsImVtYWlsIjoiYWRtaW5AZXhhbXBsZS5jb20iLCJ1c2VybmFtZSI6ImFkbWluIiwidXNlcl9pZCI6MX0.xWlhwgzzVjDwgTPp48AgAYDJnraGThlkGmBnJbKnA74'

    {
        "due_to": "2016-10-18T19:12:01Z",
        "id": 5,
        "person": 1,
        "title": "Next one"
    }

Use case

- JSON Web Tokens in urls
- Other blog posts in this series
- Use case

Nowadays when a user creates an account he or she has to confirm identity. It is done by sending an email with the link to confirm and activate an account.
As this link has to expire and be safe this is a good use case for using JSON Web Tokens. Such tokens can be generated for every user and set to expire for example after two hours. How can it be done in Django? Let's jump into the code.

#### JSON Web Tokens in urls

    from users.views import UserViewSet, CreateUserView,
    urlpatterns = [
        # rest of url patterns
        url('^api-register/$', CreateUserView.as_view()),
    ]

CreateUserView looks as follows:

    from rest_framework import status
    from rest_framework.generics import CreateAPIView
    from rest_framework.response import Response
    from rest_framework_jwt.settings import api_settings

    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    class CreateUserView(CreateAPIView):

        model = User.objects.all()
        permission_classes = [
            permissions.AllowAny # Or anon users can't register
        ]
        serializer_class = UserSerializer

        def create(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            user = self.model.get(username=serializer.data['username'])
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return Response(
                {
                    'confirmation_url': reverse(
                        'activate-user', args=[token], request=request
                    )
                },
                status=status.HTTP_201_CREATED, headers=headers
            )

Add few additional lines for creating JWT. First I created payload by adding user to JWT creation process, then I created the token from payload by calling jwt_encode_handler. At the end instead of returning user data, I return confirmation_url for the end user to enter and activate the account. By default django make every user active so I have to write my own create method for UserSerializer:

    from django.contrib.auth.models import User
    from rest_framework import serializers
    from tasks.models import Task

    class UserSerializer(serializers.ModelSerializer):
        tasks = serializers.PrimaryKeyRelatedField(
            many=True, queryset=Task.objects.all()
        )

        class Meta:
            model = User
            fields = ('username', 'password', 'tasks', 'email')

        def create(self, validated_data):
            user = User(
                email=validated_data['email'],
                username=validated_data['username']
            )
            user.set_password(validated_data['password'])
            user.is_active = False
            user.save()
            return user

$ http POST 127.0.0.1:9000/api-register/ username=user_name password=your_pass email=your.email@abc.com

    {
        "confirmation_url": "http://127.0.0.1:8000/api-activate/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImtyenlzenRvZkBrei5jb20iLCJ1c2VyX2lkIjoyNSwidXNlcm5hbWUiOiJrcnp5c2llayIsImV4cCI6MTQ3OTA1MDQ5M30.CMcW8ZtU6AS9LfVvO-PoLyqcwi6cOK1VzI2o7pEPX2k/"
    }

How this confirmation_url works? I made additional urlpattern:

    from users.views import ActivateUser

    urlpatterns = [
        # rest of url patterns
        url(
            '^api-activate/(?P<token>.+?)/$',
            ActivateUser.as_view(),
            name='activate-user'
        ),
    ]

and in ActivateUser:

    class ActivateUser(APIView):

        def get(self, request, *args, **kwargs):
            token = kwargs.pop('token')
            try:
                payload = jwt_decode_handler(token)
            except jwt.ExpiredSignature:
                msg = _('Signature has expired.')
                raise exceptions.AuthenticationFailed(msg)
            except jwt.DecodeError:
                msg = _('Error decoding signature.')
                raise exceptions.AuthenticationFailed(msg)
            except jwt.InvalidTokenError:
                raise exceptions.AuthenticationFailed()

            user_to_activate = User.objects.get(id=payload.get('user_id'))
            user_to_activate.is_active = True
            user_to_activate.save()

            return Response(
                {'User Activated'},
                status=status.HTTP_200_OK
            )

In get simply take the token from kwargs and perform validation on that token - if it's valid or expired.

$ http GET http://127.0.0.1:8000/api-activate/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImtyenlzenRvZkBrei5jb20iLCJ1c2VyX2lkIjoyNSwidXNlcm5hbWUiOiJrcnp5c2llayIsImV4cCI6MTQ3OTA1MDQ5M30.CMcW8ZtU6AS9LfVvO-PoLyqcwi6cOK1VzI2o7pEPX2k/

    [
        "User Activated"
    ]

$ http GET http://127.0.0.1:8000/api-activate/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImtyenlzenRvZkBrei5jb20iLCJ1c2VyX2lkIjoyNSwidXNlcm5hbWUiOiJrcnp5c2llayIsImV4cCI6MTQ3OTA1MDQ5M30.CMcW8ZtU6AS9LfVvO-PoLyqcwi6cOK1VzI2o7pEPX2k/

    {
     "detail": "Signature has expired."
    }

By default django rest framework jwt sets token expiry time to 5 minutes. If you want to change that add following lines in settings.py:

    JWT_AUTH = {
         'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=7)
    }

### Reference:

* https://krzysztofzuraw.com/blog/2016/jwt-in-django-application-part-one.html
[1]: https://docs.djangoproject.com/en/dev/_modules/django/apps/config/#AppConfig.get_model
[1]: https://tools.ietf.org/html/rfc7519
[2]: http://blog.apcelent.com/images/json-web-token-authentication-apcelent.png

