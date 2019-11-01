# Token Authentication in Django Rest Framework

Add this into your settings.py:
```python
INSTALLED_APPS = [
    # Your other apps
    'rest_framework.authtoken',
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': int(os.getenv('API_PAGE_SIZE', 100)),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}
```
then;
`$ python manage.py migrate`

Add 2 lines of code into your View class:
```python
# Add these import statements
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class BuildTrigger(APIVIew):
    authentication_classes = (TokenAuthentication,) # Add this line
    permission_classes = (IsAuthenticated,)         # Add this line
    # Your remaining code
```
At this moment if you try to access your endpoints, you will get an error message like 'Authentication credentials were not provided.'
There are 2 steps involved in order to gain access to the endpoint:

1. Generate a Token

`$ python manage.py shell`
```python
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
user = User.objects.get(username="your_username")
token = Token.objects.create(user=user)
token.key
```
OR
`$ python manage.py drf_create_token -r <your_username>`

2. Supplying the Token

`curl -X GET http://127.0.0.1:10000/api/ -H 'Authorization: Token caff37f830e5bd8283830ad5fc5f1aa226120cb8'`

