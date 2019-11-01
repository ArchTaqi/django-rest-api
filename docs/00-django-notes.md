# Overview

- Restful specification (recommended)
- Django Rest Framework framework

#知识点回

## Development mode

- Ordinary development method (write the front and rear ends together)
- Front and rear separation

## Backend development

- Provide a URL for the front end (API/interface development)
- Note: Always return HttpResponse

## Django URL request processing method (FBV, CBV)

- **Internal implementation principle**
  - The essence of HTTP requests is based on sockets.

```python
#知识点补充- getattr
# getattr(object, name[,default]) function is used to obtain the property or method of the object object
# Syntax:
    getattr(object, name[, default])
'''
parameter
    Object - object
    2. name - string, object attribute
    3. default - the default return value, if this parameter is not provided, AttributeError will be triggered when there is no corresponding attribute
'''

class A(obj):
    bar = 1

a = A()
Print(getattr(a, 'bar')) # print "1"
Print(getattr(a, 'attr', 2)) # attribute attr does not exist, but default value is set, print "2"
```

- **FBV - Function Base View**

```python
#路由
url(r'^xx/', views.users)

# view
def users(request):
    if request.method == "GET":
        pass
    elif request.method == "POST":
    return HttpResponse(json.dumps(...))
```

- **CBV - Class Base View**
  - Essence: Based on the reflection implementation, different methods are executed depending on the request method.
    - Syntax: getattr(object, request.method), to match methods in some objects
    - Principle: url -> view method -> dispatch method (reflection execution other: GET/POST/PUT/PATCH/DELETE/HEAD/TRACE/OPTIONS)
    - django built-in module: **django.views.generic.base**
  - Process:
    ``Request`
    2. `Routing (as_view method)`
    3. `view method`
    4. `dispatch method (with reflection inside)`
  - Tips:
    - Cancel the CSRF Toekn authentication method, the decorator should be added to the dispatch method, and the method_decrator decoration is required.

```python
#路由
url(r'^xx/', views.StudentView.as_view())

# view
from django.views import View
class MyBasicView(object):
    def dispatch(self, request, *args, **kwargs):
        print('before')
        ret = super(MyBasicView, self).dispatch(request, *args, **kwargs)
        print('after')
        return right

class StudentView(MyBasicView, View):
    #方式3: Annotation dispatch method
    def dispatch(self, request, *args, **kwargs):
        #方式1
        '''
        func = getattr(self, request.method)
        ret = func(request, *args, **kwargs)
        return right
        '''
        #方式2
        '''
        ret = super(StudentsView, self).dispatch(request, *args, **kwargs)
        return right
        '''
    def get(self, request, *args, **kwargs):
        pass
    def post(self, request, *args, **kwargs):
        pass
    def put(self, request, *args, **kwargs):
        pass
    def dete(self, request, *args, **kwargs):
        pass
```

## List generation

```python
class Foo：
    pass

class Bar:
    pass

#对象列表- mode 1
v = [item() for item in [Foo, Bar]]

#对象列表- mode 2
v = []
for i in [Foo, Bar]:
    obj = i()
    v.append(obj)
```

## Object Oriented

- Polymorphism
- Inheritance: The ability to share multiple classes, in order to avoid repeated writing
- Packaging
  - Encapsulate the same class method into ** class**
  - Encapsulate data into ** objects**

```python
class File
    #File addition, deletion and change method
    def __init__(self, age, address):
        self.age = age
        self.address = address
    def get():
        pass
    def delete():
        pass
    def update():
        pass

class DB:
    #方法方法

obj1 = File (17, 'SZ')
Obj2 = File(18, 'GZ') # Encapsulate data 18 and 'GZ' into an object
```

```python
class Request(object):
    def __init__(self, obj):
        self.obj = obj

    @property # Here when you execute the user function, you don't need to add ()
    def user(self):
        return self.obj.authicate()

class Auth(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def authticate(self):
        return self.name
        # return True

class APIView(object):
    def dispatch(self):
        self.f2()
    def f2(self):
        a = Auth('alex', 18)
        b = Auth('andrew', 18)
        # req = Request(a)
        req = Request(b)
        Print(req.obj) # Auth object
        Print(req.user) # print True

obj = APIView()
obj.dispatch()
```

## Interview questions

- What is the **django middleware function? (up to 5 methods)**
  - `process_request`
  - `process_view`
  - `process_response`
  - `process_exception`
  - `process_render_template`
- **What have you done with middleware**
  - Permissions
  - User login verification
  - Django's CSRF Token (how to do it?)
    - Middleware-based **process_view method** certification
      - Get the token in the request body or cookies, and then check against the token
      - Determine whether a random string is present before executing the view function; or check if the view is decorated with @csrf_exempt (representing exemption from csrf authentication). Because in the **process_request method**, the view function has not been obtained, so if you need to use the decorator such as csrf_excempt, you must put it in the processes_view method.
    - Decorator sets individual functions (authentication or no authentication required)
- **Two ways to set CSRF token**
  - Middleware
  - Decorator

```python
# Case 1: Global use of certification, some do not require certification
# settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware', # all stations use csrf authentication
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# view - FBV
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def users(request):
    pass

# view - CBV - way 1
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

class StudentView(MyBasicView, View):
    @method_decorator(csrf_exempt) # must be decorated in the dispatch method, not decorated in other separate methods
    def dispatch(self, request, *args, **kwargs):
        ret = super(StudentsView, self).dispatch(request, *args, **kwargs)
        return right
    def get(self, request, *args, **kwargs):
        pass
    def post(self, request, *args, **kwargs):
        pass
    def put(self, request, *args, **kwargs):
        pass
    def dete(self, request, *args, **kwargs):
        pass

# view - CBV - way 2
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class StudentView(MyBasicView, View):
    def dispatch(self, request, *args, **kwargs):
        ret = super(StudentsView, self).dispatch(request, *args, **kwargs)
        return right
    def get(self, request, *args, **kwargs):
        pass
    def post(self, request, *args, **kwargs):
        pass
    def put(self, request, *args, **kwargs):
        pass
    def dete(self, request, *args, **kwargs):
        pass

```

```python
# Case 2: Global does not use authentication, some use authentication
# settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# view - FBV
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def users(request):
    pass
```

#interface development mode

Starting point: Add, delete, and check a certain resource! Backend development interface to the front end call

## Normal mode (not Restful)

- Question:
  - Different actions for different resources (additions, deletions, and changes) for the same resource
  - The number of URLs will be more and more (for example, adding, deleting, and changing 10 tables, basically there are 40 URLs)
  - Personal feeling:
    - Is to issue a request for an operation mode and then consider the resource. For example: `I want to do the query operation, for the order resource`

```python
#路由
url(r'^get_order/', views.get_order)
url(r'^add_order/', views.add_order)
url (r '^ del_order /', views.del_order)
url(r'^update_order/', views.update_order)

# view
def get_order(request):
    return HttpResponse('')

def add_order(request):
    return HttpResponse('')

def del_order(request):
    return HttpResponse('')

def update_order(request):
    return HttpResponse('')
```

## Restful specification (recommended)

- For the above common mode, agreed specifications and recommendations
  - Make the interface respond differently depending on the request.method
  - Important: For one piece of data (one order), one URL
    - How to distinguish between additions, deletions and changes? According to the difference of methods!
  - Personal feeling:
    - Is a request operation for a resource. For example: `I want to do query operations for order resources.

```python
#路由
url(r'^order/', views.order)

# FBV mode - view - do different operations depending on the method
def order(request):
    if request.method == "GET":
        Return HttpResponse('Get Order')
    elif request.method == "POST":
        Return HttpResponse('new order')
    elif request.method == "PUT":
        Return HttpResponse('update order')
    elif request.method == "DELETE":
        Return HttpResponse('delete order')
```

```python
#路由
url(r'^order/', views.OrderView.as_view())

# CBV mode - view
from django.views.generic import View
class OrderView(View):
    def get(self, request, *args, **kwargs):
        Return HttpResponse('Get Order')
    def post(self, request, *args, **kwargs):
        Return HttpResponse('new order')
    def put(self, request, *args,, **kwargs):
        Return HttpResponse('update order')
    def delete(self, request, *args,, **kwargs):
        Return HttpResponse('delete order')
```

### Detailed specification

Reference: `http://www.cnblogs.com/wupeiqi/articles/7805382.html`

- ** API and user communication protocol, always use HTTPS protocol (recommended)**
- **domain name**
  - How to use the `https://api.example.com` subdomain (requires cross-domain issues)
  - `https://example.org/api/` URL method (same domain name, just different URLs)
- **Version**
  - URL (recommended)
    - `https://example.org/api/v1/`
    - `https://example.org/api/v2/`
    - `https://example.org/api/v3/`
  - Request header
- ** Resource-oriented programming**
  - Essence: Think of anything on the network as a ** resource (both in nouns or plurals)**. You can add, delete, or change this resource.
  - https://example.org/api/v1/zoos
  - https://example.org/api/v1/animals
  - https://example.org/api/v1/employees
- **Request Method**
  - GET: Remove resources (one or more) from the server
  - POST: Create a new resource on the server
  - PUT: Update resources on the server (the client provides the changed full resources)
  - PATCH: Update resources on the server (the client provides changed properties)
  - DELETE: delete resources from the server
- **Filter, pass search criteria in the form of url upload parameters**
  - `https://example.org/api/v1/zoos?limit=10: Specify the data to return the record.
  - `https://example.org/api/v1/zoos?offset=10: Specify the starting position of the return record.
  - `https://example.org/api/v1/zoos?page=2&per_page=100: Specify the first few pages, and the number of records per page.
  - `https://example.org/api/v1/zoos?sortby=name&order=asc: specifies which attribute to return the results to sort, and the sort order.
  - `https://example.org/api/v1/zoos?animal_type_id=1: Specify filter criteria`
- **status code**
  - `Action`: use the status code to prompt the user
  - `Question`: The status code is not enough. For example, when creating a data, various errors may occur when it is created. For example, the returned data does not exist, the data is not found, the data is being used, and the status of the data is many. So when we use the API to return, we will use the code field to do the status code to indicate more status.
  - `Use `: General status code combined with code
  - `Note`: Generally do interface development, ask if the front end needs a status code?
  - `Series`
    - 200 Series: Success
    - 300 Series: Redirection
    - 400 Series: Client Error
    - 500 Series: Server Error

```python
#General status code combined with code
class OrderView(View):
    def get(self, *args, **kwargs):
        right = {
            'code': 1000,
            'msg': 'xxx'
        }
        return HttpResponse(json.dumps(ret), status=201)
```

- **Error handling**
  - When the status code is 4xx, an error message should be returned, and error is used as the key.

```json
{
    error: "Invalid API Key"
}
```

- **Return results, the results returned by the server to the user for different operations should meet the following specifications** (/collection/resource)
  - GET /order/: return a list of resource objects (array)
  - GET /order/1/: return a single resource object
  - POST /order/: return the newly generated resource object
  - PUT /order/1/: return full resource object
  - PATCH /order/1/: return the full resource object
  - DELETE /order/1/: return an empty document
  
- **Hypermedia API**, RESTful API is best to do Hypermedia, which provides links in the returned results, connected to other API methods, so that users do not check the documents, but also know what to do next

```python
[
    {
        id: 1,
        name: 'A',
        price: xx,
        url: 'http://xxx.com/1/'
    },
    {
        id: 2,
        name: 'B',
        price: xx,
        url: 'http://xxx.com/2/'
    }
]

/order/
/order/1/
```

### Your own knowledge of the Restful API specification

- It is essentially a specification that makes front-end and end-to-end interface development and use more convenient and obvious

# Supplement

## Related references

- from django.views import **View**
- from rest_framework.views import **APIView**
- from rest_framework.request import Request
- from rest_framework import exceptions
- from rest_framework.viewsets import ModelViewSet

## Summary problem
  
- Middleware
- CSRF
- CBV
- REST api specification
- django RestFramework
  - How to verify (based on database implementation user authentication)
  - Source process (object-oriented review process)
- django request life cycle
- django request life cycle (including the rest framework framework)
  - PS: **dispatchf() method**
- rest framework certification process (package Request)
- rest framework permission process
- rest framework throttling process
- Code (three component combination)
  - Certification Demo
  - Permissions Demo (user types are different, permissions are different)
  - Throttling Demo (anonymous, login)

# Django Rest Framework (1)

The APIView class in the rest_framework.views module inherits the View class of the django views module and then enriches some features.

```python
#installation
pip install djangorestframework

#码
from django.views import View
from rest_framework.views import APIView

#方式1: Inherit django native View
class OrderView(View):
    pass

#方式2: Inherit drf APIView
class OrderView(APIView):
    pass
```

Rest_framework/views.py module (reflex - dispatch method source details)

```python
'''
CBV request process (note: django.views module.View class)
    Receive request (URL)
    2. Routing (execution of as_view method)
        2.1 as_view is a method in the View class
    3. view method
        3.1 view() is the method in the as_view method
    4. dispatch method (doing reflection)
        4.1 dispatch is a method in the View class
'''

def dispatch(self, request, *args, **kwargs):
    self.args = args
    self.kwargs = kwargs
    #Processing the original request (enriched some functions)
    # Request(request, parsers=self.get_parsers(), authenticators=self.get_authenticators(), negotiator=self.get_content_negotiator(), parser_context=parser_context)
    # Request(native request, [BasicAuthentication object,...])
    request = self.initialize_request(request, *args, **kwargs)
    # Get the original request, request._request
    # Get the object of the authentication class, request.authenticators -> is a list of objects

    # 1. Package - Request
    self.request = request
    self.headers = self.default_response_headers

    try:
        # 2. Certification
        self.initial(request, *args, **kwargs)

        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(),
                                self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed

        response = handler(request, *args, **kwargs)

    except Exception as exc:
        response = self.handle_exception(exc)

    self.response = self.finalize_response(request, response, *args, **kwargs)
    return self.response
```

Preliminary understanding of DRF certification

- ** source process **
  - URL request
  - as_view() method [ `urls.py` ]
  - view()方法 [ `rest_framework\views.py` ]
  - dispatch()方法 [ `rest_framework\views.py` ]
    - initialize_request(request, *args, **kwargs)
      - **authenticators**=self.get_authenticators(),
    - initial(request, *args, **kwargs)
      - perform_authentication(request) implements authentication
        - request.user
          - self._authenticate() [ `request.py` ]
            - for authenticator in self.**authenticators**:
            - Success:
              - user_auth_tuple = authenticator.authenticate(self)
            - Failure:
              - self._not_authenticated()
      - check_permission(request) implements permission control
      - check_throttles(request) Interface access rate limit (for example: only 5 times in 1 minute)

```python

import json
from rest_framework.views import APIView
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

'''Custom authentication class'''
class MyAuthentication(object):
    def authenticate(self, request):
        # Here you can get the username and password, go to the database to check
        token = request._request.GET.get('token')
        if not token:
            # Authentication failed
            Raise exceptions.AuthenticationFailed('User authentication failed')
        #认证认证
        #元组第一元素:reqeust.user
        return ("alex", None)

    def authenticate_header(self, val):
        pass


class DogView(APIView):
    '''Custom authentication class'''
    authentication_classes = [MyAuthentication, ]

    def get(self, request, *args, **kwargs):
        print(request)
        print(request.user)
        right = {
            'code': 1000,
            'msg': 'xxx'
        }
        return HttpResponse(json.dumps(ret), status=201)
    def post(self, request, *args, **kwargs):
        return HttpResponse('创建Dog')
    def put(self, request, *args, **kwargs):
        return HttpResponse('更新Dog')
    def delete(self, request, *args, **kwargs):
        return HttpResponse('删除Dog')
```

## Supplementary Summary

- Middleware
- CSRF_Token
  - Why use the process_view function?
    - process_view is related to the view function (decorator), you need to find the view function before you can judge
- CBV mode
  - Two interface development modes
    - FBV (function view)
    - CBV (class view)
      1. **from django.views import View**
      2. **from rest_framework.views import APIView** (inherited from Django's View class)
         - from rest_framework.request import Request
         - from rest_framework import exceptions
- Key basics
  - Iterator
  - Builder
  - Reflection (Restframe work source code - dispatch method)
- Specification
  - 10 specifications
  - Detailed explanation
- DRF framework
  - How to authenticate? (Task: Implement user authentication based on database)
  - Source process (object-oriented, encapsulation and inheritance)
- django request life cycle (including the rest framework framework)

# Django Rest Framework components (2)

- Today's content (DRF component), the following source process is triggered by the **dispatch method**
  - `(identity) certification`
  - `Permissions`
  - `Throttle (access rating control)`
  - `Version processing`

## Certification

### question

Some APIs require users to log in successfully before they can access them, while others do not.

### Basic use components

- Customize the authentication class in the view function, but drf also supports global configuration authentication class

```python
from api import models
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework import exceptions

ORDER_DICT = {
    1: {
        'name': '媳妇',
        'age': 18,
        'gender': 'male',
        'content': '...'
    },
    2: {
        'name': 'Old dog',
        'age': 19,
        'gender': 'male',
        'content': '...'
    }
}


def md5(username):
    # Generate md5 value based on user name
    import hashlib
    import time
    ctime = str(time.time())
    # encoding with utf-8, converted to bytecode
    m = hashlib.md5(bytes(username, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()


# login request - generate a token for the matching user
class AuthView(APIView):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello Get")
    def post(self, request, *args, **kwargs):
        # print(dir(request._request.POST))
        try:
            ret = {'code': 1000, 'msg': None}
            # Very note here rqeuest._request.POST
            username = request._request.POST.get('username')
            password = request._request.POST.get('password')
            obj = models.UserInfo.objects.filter(username=username, password=password).first()
            if not obj:
                ret['code'] = 1001
                Ret['msg'] = "The username or password is incorrect"
            # Create a Token (random string) for the logged in user
            else:
                token = md5(username)
                models.UserToken.objects.update_or_create(user=obj, defaults={'token': token})
                ret['token'] = token
        except Exception as e:
            ret['code'] = 1002
            Ret['msg'] = "Request exception"
        return JsonResponse(ret)

#定制认证类
class Authentication(object):
    def authenticate(self, request):
        # After analyzing the DRF dispatch function, I know that I can write custom authentication here.
        token = request._request.GET.get('token')
        token_obj = models.UserToken.objects.filter(token=token).first()
        if not token:
            Raise exceptions.AuthenticationFailed('User authentication failed')
        # In the rest framework, these two fields will be assigned to the request for subsequent operations.
        # request.user - the first element of the assigned tuple
        # request.auth - the second element of the assigned tuple
        return (token_obj.user, token_obj)

    def authenticate_header(self, request):
        pass

class OrderView(APIView):
    authentication_classes = [Authentication, ]

    def get(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None, 'data': None}
        try:
            ret['data'] = ORDER_DICT
        except Exception as e:
            pass
        return JsonResponse(ret)

class UserInfoView(APIView):
    authentication_classes = [Authentication, ]

    def get(self, request, *args, **kwargs):
        Return HttpResponse("User Information")
```

### Certification Basic Process Source Code Analysis

- DRF certification request execution process
  - request
  - Routing
  - APIView - dispatch method
  - Step 1: Request package [`initialize_request()`]
    - Method 1: request encapsulates the authenticators - authentication_classes (by default in the configuration file)
    - Method 2: Customize the authentication class to implement two methods: authenticate and authenticate_header
  - Step 2: Certification [`initial()`]
    - perform_authticate()
    - request.user (Note: user may be a method because it is decorated with property)
      - Loop ** all objects of the authentication class** and execute the authenticate method of the authentication class
        1. If the authenticate method throws an exception, self._not_authenticated() executes
        2. `There is a return value, it must be a tuple: (request.user, request.auth)`
        3. No error, no return value, defaults to None. Then loop the next authentication object processing
        4. If there is no authentication, self.user and self.auth have default values ​​api_settings(AnonymouaUser/None)
  - `Reflection` function
  - view functions (get, post, put, patch, delete)
  - Execute business logic code

![avatar](/statics/Authentication.png)

### Built-in authentication

- Classification (BaseAuthentication)
  - **BasicAuthentication**
  - Based on django (session, token)
    - **SessionAuthentication**
    - ** TokenAuthentication **
    - **RemoteUserAuthentication**
  - Custom authentication class (must inherit from the BaseAuthentication class)
    - Implement the authenticate() method
    - Implement the authenticate_header() method

- Use steps and details
  - Create class: Inherit BaseAuthentication to implement the authenticate method
  - return value:
    - None, the next authentication class to execute, if it is None, it is an anonymous user
    - Throw an exception, rase exception.AuthenticationFailed("User authentication failed")
    - tuple (element 1, element 2), element 1: request.user, element 2: request.auth
  - Global calls and local calls
    - Partial: Write a static field in the view class
    - Global: Profile
      - DEFAULT_AUTHENTICATION_CLASSES
      - UNAUTHENTICATED_USER
      - UNAUTHENTICATED_TOKEN

- Source process
  - request
  - dispatch
    - **request package**
      - Get all defined authentication classes, create objects by list generation
    - **initiual() - Certification**
      - perform_authentication()
        - request.user
          - Encapsulation object encapsulated in the request
          - Cyclic authentication object
          - Judgment

```python
# from rest_framework.authentication import BaseAuthentication

class BaseAuthentication(object):
    ...
    def authenticate(self, request):
        pass
    def authenticate_header(self, request):
        # When the authentication fails, the returned request header is processed.
        pass

# Based on the browser implementation pop-up box (generally not applicable to this class)
class BasicAuthentication(BaseAuthentication):
    pass
```

## Permissions

### question

- Can the distinction of permissions be done on the view? How to distinguish permissions?
  - Each user object has a type field!
- Different views can be accessed with different permissions?

### Basic use

- Step 1: Create a permission permission class, you must inherit the BasePermisson class, and you must implement the has_permission() method.
  - Return value: True, False, None
- Step 2: Then refer to the view view
  - **permission_classes = [...]**
- Step 3: Global configuration
  - **"DEFAULT_PERMISSION_CLASSES": ['...', ]**

```python
# permission.py
class MyPermission(object) {
    def has_permission(self, request, view):
        if request.user.user_type ....
        ...
        return True
}

# views.py
from api.utils.permission import MyPermission
class XXX(APIView):
    # authentication_classes = [Authentication, ]
    permission_classes = [MyPermission, ]

    def get(self, request, *args, **kwargs):
        pass
```

### Source Process

- Routing request
- dispatch方法（rest_framework/views.py）
  - Package request
  - initial() method
    - perform_authentication() # Implement authentication
    - check_permissions() # permission judgment
      - get_permissions() returns a list of objects of the permission class
  
### Built-in permissions

Is there a permission for the built-in? (rest_framework/permissions.py)

- class BasePermission(object)
- class AllowAny(BasePermission)
- Based on Django's permission class (generally not recommended for direct use!)
  - class IsAuthenticated (BasePermission)
  - Classifieds Ads (BasePermission)
  - class IsAuthenticatedOrReadOnly (BasePermission)
  - class DjangoModelPermissions (BasePermission)
  - class DjangoModelPermissionsOrAnonReadOnly(DjangoModelPermissions)
  - class DjangoObjectPermission
  - (DjangoModelPermissions)

### Summary

- permission to control the location of the write
  - Middleware
  - view
  - custom class for restframe work

## Control access frequency - throttling

### customize

Question: A user, his access frequency to do a control, such as 1 minute can only access 3 times, if 3 times within 1 minute to access, give the user a hint and countdown seconds on the next visit

```python
from rest_framework.throttling import BaseThrottle
import time

VISIT_RECORD = {} # can be placed in the django cache

#定制认证类
#定制权限类
#定制限制类
class VisitThrottle ():
    """
    Can only access 3 times in 60 seconds
    """

    def __init__(self):
        self.history = None

    def allow_request(self, request, view):
        # 1. Get user IP
        # remote_addr = request._request.META.get('REMOTE_ADDR')
        # remote_addr = request.META.get('REMOTE_ADDR')
        Remote_addr = self.get_ident(request) # Get the IP address
        ctime = time.time()
        if remote_addr not in VISIT_RECORD:
            VISIT_RECORD[remote_addr] = [ctime, ]
            return True
        history = VISIT_RECORD.get(remote_addr)
        self.history = history

        while history and history[-1] < ctime - 60:
            history.pop()

        if len(history) < 3:
            # [ 12:10:07, 12:10:06, 12:10:05, .. ]
            history.insert(0, ctime)
            return True
        # return True / return False indicates that the access frequency is too high and is limited

    def wait(self):
        # return None Tip: How many seconds do you need to wait?
        ctime = time.time()
        return 60 - (ctime - self.history[-1])

# view (partial mode)
class AuthView(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = [VisitThrottle,]

    def post(..):
        pass
```

### Built-in frequency control class (throttling.py)

- **SimpleRateThrottle**
  - By modifying the configuration file, you can customize how many times to limit the number of accesses in seconds.

```python
# throttle.py

#定制限制类一
class VisitThrottle (SimpleRateThrottle):
    scope = "Luffy"
    # Must be overridden
    def get_cache_key(self, request, view):
        return self.get_ident(request)

#定制限制类二
class UserThrottle(SimpleRateThrottle):
    scope = "LuffyUser"
    # Must be overridden
    def get_cache_key(self, request, view):
        return request.user.username

# settings.py(global mode)
REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_RATES": {
        "Luffy": '3/m', #3 times per minute
        "LuffyUser": '10/m'，
    }
}
```

- AnonRateThrottle
- UserRateThrottle
- ScopedRateThrottle

### Summary

The above method can only control a part, and his IP can be changed for anonymous users. For registered users, many users can be registered.

- Basic use:
  - Method 1: Customize the restriction class, inherit the BaseThrottle built-in class, implement the allow_request, wait method s
  - Method 2: Inherit the built-in class, SimpleRateThrottle, implement get_cache_key, scope="xxx" (key in the configuration file!)

# Django Rest Framework components (3)

Summary of contents (the remaining 7 components of DRF):

- **Version**(*)
- **Parser**(*) (essentially parsing the data in the request body)
- **Serialization**(*****)
  - Verify request data
  - Serialize QuerySet
- **Page **(**)
- **Route**(**)
- **View**(**)
  - rest_framework.views
    - APIView (requires inheritance)
  - rest_framework.viewsets
    - ModelViewSet (requires inheritance)
      - mixins.CreateModelMinxin
      - mixins.RetrieveModelMixin
      - mixins.UpdateModelMixin
      - mixins.DestroyModelMixin
      - mixins.ListModelMixin
      - GenericViewSet
        - ViewSetMixin
        - generics.GenericAPIView
          - views.APIView
- **Renderer**(*)

Content review:

- Encapsulation, inheritance, polymorphism (object-oriented)
- Django life cycle
  - `wsgi` agreement
  - `wsgiref` implements the module of the wsgi protocol, the essence of which is a socket server
  - `werkzeug` module (Flask framework)
  - `tornado` (completely implement the socket yourself)
  - `uwsgi` module (django online deployment)
- Django Lifecycle (CBV/DRF)
- Middleware & Decorators
  - Uniform operation on all requests
  - Scenario: role-based user rights management (RBAC), user authentication, csrf, session, blacklist, logging;
- Rest framework principle
  - `Certification process`
    - authenticate
    - authenticate_header
  - `Permissions Process`
    - has_permission
  - `Throttle flow'
    - Anonymous can be based on IP or proxy, login users can be based on username
    - allow_request
    - wait

##版

### Basic use and implementation

Where can the version be placed?

- on the URL
- GET pass
- Subdomain
- namespace
- Request header

Version control class (rest_framework.versioning)

- BaseVersioning
- QueryParameterVersioning
- URLPathVersioning

achieve

- Method 1: Pass the GET parameter in the URL - customize the class to implement the determine_version method
- Method 2: Pass parameters in the URL path, such as /api/v1/users, /api/v2/users, etc.

```python
# method 1
url(r'^api/v1/order/$', views.OrderView.as_view())
url(r'^api/v1/info/$', views.UserInfoView.as_view())


#方法2: Passing GET on the URL
def get(self, request, *args, **kwargs):
    version = request.query_params.get('version')
    return HttpResponse('')


#方法3:versioning(DRF)
# 访问:http://127.0.0.1:8000/api/users?version=v2
class ParamVersion(object):
    def determine_version(self, request, *args, **kwargs):
        # Get parameter data in the request
        version = request.query_params.get('version')
        return version

class UsersView(APIView):
    versioning_class = 'ParamVersion'

    def get(self, request, *args, **kwargs):
        # (Important) After customizing the class, after adding it through the versioning_class, there will be a version attribute in the request object to record the version number.
        print(request.version)
        return HttpResponse('')

#方法4:
from rest_framework.versioning import BaseVersioning, QueryParameterVersioning, URLPathVersioning

class UsersView(APIView):
    versioning_class = 'QueryParameterVersioning'

    def get(self, request, *args, **kwargs):
        print(request.version)
        return HttpResponse('')

#settingConfiguration
REST_FRAMEWORK = {
    "DEFAULT_VERSION": 'v1', # default version
    "ALLOWED_VERSIONS": ['v1','v2'], # allowed version
    "VERSION_PARAM": 'version' # version key of the parameter
}

#方法5 (recommended)
# Visit: http://127.0.0.1:8000/api/v1/users
urlpatterns = [
    url(r'^(?P<version>[v1|v2]+)/users/$', users_list, name='users-list'),
    url(r'^(?P<version>[v1|v2]+)/users/(?P<pk>[0-9]+)/$', users_detail, name='users-detail')
]

class UsersView(APIView):
    versioning_class = 'URLPathVersioning'

    def get(self, request, *args, **kwargs):
        print(request.version)
        return HttpResponse('')
```

```python
# This version is available after a one-time configuration, generally configured globally in the settings configuration file
# omitted to add the versioning_class attribute to each view
REST_FRAMEWORK = {
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    "DEFAULT_VERSION": 'v1', # default version
    "ALLOWED_VERSIONS": ['v1','v2'], # allowed version
    "VERSION_PARAM": 'version' # version key of the parameter
}

# view
# DRF方法
Request.version (get version)
Request.versioning_schema (get the object of the processed version)
# Reverse generated URL (REST FRAMEWORK)
Request.versioning_schema.reverse(viewname='the value of the name attribute on the URL', request=request)

# Reverse generated URL (Django original method)
from django.urls import reverse
Reverse(viewname='the value of the name attribute on the URL', kwargs={'version': 2})
```

### to sum up

Use - configuration file

```python
REST_FRAMEWORK = {
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    "DEFAULT_VERSION": 'v1', # default version
    "ALLOWED_VERSIONS": ['v1','v2'], # allowed version
    "VERSION_PARAM": 'version' # version key of the parameter
}
```

Use - routing system

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls'))
]

urlpatterns = [
    re_path('^(?P<version>[v1|v2|v3]+)/users/$', views.UsersView.as_view()),
]
```

Use - view

```python
class UsersView(APIView):
    # self.dispatch
    # 1. Get the version
    print(request.version)

    # 2. Get the processed version of the object
    print(request.versioning_schema)

    # 2.1 Reverse Generate URL (DRF)
    u1 = request.versioning_schema.reverse(viewname='uuu', request=request)

    # 2.2 Reverse generated URL (Django built-in)
    u2 = reverse(viewname='uuu', kwargs={'version': 2})

    return HttpResponse('')
```

## parser

Function: Parse the data in the user request body, and parse the data of the user request body by the request header content-type. Parse into request.data (triggered by request.data)

### Django Parser

The following two requirements are met, and there is a value in the request POST; since django internally parses the request body, it only corrects when the following two bars are satisfied at the same time.

1. **Request header request**
    If the Content-Type: application/x-www-form-urlencoded in the request header has a value in request.POST (resolve the data in request.body)

2. **Data format requirements**
   name=alex&age=18&gender=男

```python
# a. form submission
<form method...>
    input
</form>

# ajaxsubmission
$.ajax({
    url: ...,
    type: POST,
    Data: {name:alex, age=18} #internal conversion name=alex&alex=18&gender='male' with Content-Type: application/x-www-form-urlencoded header
})

# The following two cases have a value of body, POST no
$.ajax({
    url: ...,
    type: POST,
    headers: {'Content-Type': "application/json"},
    data: {name:alex, age=18}
})
$.ajax({
    url: ...,
    type: POST,
    headers: {'Content-Type': "application/json"},
    data: JOSN.stringfy({name:alex, age=18})
})

# Solution (General)
#处理 the json string in request.body
json.loads(request.body)
```

```python
from rest_framework.request import Request
from django.core.handlers.wsgi import WSGIRequest
from django.http.request import HttpRequest

class TempView(APIView):
    print(request._request)
    return HttpResponse('')
```

### Rest Framework Parser

Parse the request body data

```python
from rest_framework.parsers import JSONParser, FormParser
'''
1. JSONParser: indicates that only content-type: application/json headers (most commonly used) can be parsed, otherwise an error is reported.
2. FormParser: indicates that only the content-type:application/x-www-form-urlencode header can be parsed, otherwise an error is reported.
'''
class ParserView(APIView):
    parser_classes = [JSONParser, ]
    '''
    Allow users to send data in JSON format
        a. content-type: application/json - 头
        b. {'name':'alex', age:18} - data
    '''
    def post(self, request, *args, **kwargs):
        # Get the parsed result (only when it is used to parse - trigger parsing)
        Print(request.data) # type: dictionary
        '''
        1. Get the user request header
        2. Get the user request body
        3. According to the user request header and the request header supported in parser_classes for comparison, whoever meets it will be processed
        4. JSONParse object to process the request body
        5. Assignment to request.data
        '''
        return HttpResponse('ParserView')
```

 See the source code in request.data, how to trigger parsing

```python
from rest_framework.request import Request

...skip
@property
def data(self):
    if not _hasattr(self, '_full_data'):
        self._load_data_and_files()
    return self._full_data
...skip

```

```python
# settings.pyGlobal Configuration
REST_FRAMEWORK = {
    "DEFAULT_PARSER_CLASSES": ['rest_framework.parsers.JSONParser', 'rest_framework.parsers.FormParser']
}
```

to sum up:

- Configuration - Global configuration `settings.py`
- Use - request.data value

Source Code Process & Essence:

- **Nature**
  - Different parsers to handle according to the content-type of the request header
- ** source process **
  - dispatch
  - request encapsulation (encapsulate all parsers into the request)
  - Take authentication and so on (the root parser does not matter)
  - Execute the view function by reflection
  - Call request.data, get the parser again, and judge according to the request
  - Execute the parser function

Question (important):

Status code
2. Request header related parameters
   1. content-type
   2. refer to the anti-theft chain
   3. cookies
   4. status status code
   5. URL
   6. user-agent
   7. host
   8. accept receiving type
3. Request method
   1. get post put delete patch options

## Serialization (emphasis)

### Serialization reasons

QuerySet needs to be serialized! The data obtained from the database is converted to JSON and returned to the user.

### Two major functions

- Serialize the queryset (the format of the data obtained from the database)
- Verify the data requested by the user

Note: **JSON method can only serialize the basic data type in python**

```python
# method one:
# JSON can only serialize basic data types in python
# and queryset is a class defined in django
class RolesView(APIView):
    def get(self, request, *args, **kwargs):
        roles = models.Role.objects.all().values('id', 'title')
        roles = list(roles)
        Ret = json.dumps(roles, ensure_ascii=False) # str type
        return HttpResponse(ret)

#方式二:
from rest_framework import serializers

class RolesSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()

class RolesView(APIView):
    def get(self, request, *args, **kwargs):
        roles = models.Role.objects.all()
        ser = RolesSerializer(instance=roles, many=True)
        # ser.data is already the result of the conversion completed
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)
```

### Typical example one: serializers.Serializer

- Note a few points:
  - source is used to define which data is taken in the database (corresponding to the fields in the database)
  - **source source principle **: find the `row> object of each line (for example: UserInfo object (1)), then execute row.user_type, then retrieve the data from the database
  - (SerializerMethodField) If there is manytomany, the source is fine granular; custom display; if there is some data can not be obtained by source, you can customize the method

```python
# models.py
class UserInfo(models.Model):
    user_type_choices = (
        (1, 'Ordinary User'),
        (2, 'VIP'),
        (3, "SVIP"),
    )
    user_type = models.IntegerField(choices=user_type_choices)
    username = models.CharField(max_length=32, unique=True)
    password = models.CharFiled(max_length=64)
    group = models.ForeignKey('UserGroup', on_delete="")
    roles = models.ManyToManyField('Role')

# views.py
class UserInfoSerializer(serializers.Serializer):
    user_type_id = serializers.CharField(source="user_type")
    user_type_chi = serializers.CharField(source="get_user_type_display")
    username = serializers.CharField()
    password = serializers.CharField()
    gp = serializers.CharField(source="group.title")
    roles = serializers.SerializerMethodField()

    def get_roles(self, row):
        # print("==", row.user_type)
        # print("==", row.get_user_type_display())
        role_obj_list = row.roles.all()
        right = []
        for item in role_obj_list:
            ret.append({'id': item.id, 'title': item.title})
        return right

class UserInfoView(APIView):
    def get(self, request, *args, **kwargs):
        users = models.UserInfo.objects.all()
        ser = UserInfoSerializer(instance=users, many=True)
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)
```

### Typical Example 2: serializers.ModelSerializer

```python
class UserInfoSerializer(serializer.ModelSerializer):
    # Mixed use
    user_type_id = serializer.CharField(source="get_user_type_display")
    roles = serializers.SerializerMethodField()

    def get_roles(self, row):
        role_obj_list = row.roles.all()
        right = []
        for item in role_obj_list:
            ret.append({'id': item.id, 'title': item.title})
        return right

    class Meta:
        model = models.UserInfo
        # fields = "__all__"
        fields = ['id', 'username', 'password', 'user_type_chi', 'roles', 'group']

class UserInfoView(APIView):
    def get(self, request, *args, **kwargs):
        users = models.UserInfo.objects.all()
        ser = UserInfoSerializer(instance=users, many=True)
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)
```

### Typical Example 3: Custom Field Class (less useful!)

```python
class MyField(serializers.CharField):
    def to_representation(self, value):
        # Here you can customize the return data
        # But this method is generally not applicable, because the get_xxx() method can do this.
        return "Hello World"

class UserInfoSerializer(serializers.ModelSerializer):
    x1 = MyField(source='username')

    class Meta:
        model = models.UserInfo
        fields = ['x1']
```

### Serialization depth control (depth)

Automatic serialization of the table!

```python
class UserInfoSerializer(serializers.ModelSerializezr):
    class Meta:
        model = models.UserInfo
        # fields = "__all__"
        fields = ['id', 'username', 'password', 'group', 'roles']
        Depth = 1 # Official recommendation: 0 ~ 10 layers
```

### Serialization to generate hypermedialink (not many application scenarios)

Generate link

```python
# urls.py
re_path('^(?P<version>[v1|v2|v3]+)/userinfo/$', views.UserInfoView.as_view()),
re_path('^(?P<version>[v1|v2|v3]+)/group/(?P<xxx>\d+)$', views.GroupView.as_view(), name="gp"),

# views.py
class UserInfoSerializer(serializers.ModelSerializer):
    group = serializers.HyperlinkedIdentityField(view_name="gp", source="group_id", lookup_field="group_id", lookup_url_kwarg="xxx") # 反向生成URL
    class Meta:
        model = models.UserInfo
        # fields = "__all__"
        fields = ['id', 'username', 'password', 'group', 'roles']
        depth = 0

class UserInfoView(APIView):
    def get(self, request, *args, **kwargs):
        users = models.UserInfo.objects.all()
        ser = UserInfoSerializer(instance=users, many=True, context={'request': request})
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserGroup
        fields = "__all__"

class GroupView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('xxx')
        obj = models.UserGroup.objects.filter(pk=pk).first()
        ser = GroupSerializer(instance=obj, many=False)
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)
```

### Serialized source code analysis

- Object
  - Serializer class processing
- QuerySet
  - ListSerializer class processing

### Serialization Verification User Request Data

Question: When I need to customize the validation rules, do I need a hook function? How to write the hook function?

```python
class XXValidator(object):
    # Generally not playing like this because there is a hook function
    def __init__(self, base):
        self.base = base

    # As long as the data is submitted, the call method will be executed.
    def __call__(self, value):
        # value is the value submitted
        if not value.startswith(self.base):
            Message = 'The title must start with %s' % self.base
            raise serializers.ValidationError(message)


class UserGroupSerializer(serializers.Serializer):
    # Can fill in some parameters to verify this structure
    Title = serializers.CharField(error_messages={'required': 'The title cannot be empty'}, validators=[XXValidator('old man'), ])


class UserGroupView(APIView):

    def post(self, request, *args, **kwargs):
        print(request.data)
        ser = UserGroupSerializer(data=request.data)
        if ser.is_valid():
            #验证过
            print(ser.validated_data)
            print(ser.validated_data['title'])
        else:
            #验证不过
            print (be.errors)
        Return HttpResponse('submit data')
```

### Serialization Custom Validation Rule (Field Verification)

#### Verification of individual fields

- The hook method that defines the check field in the serializer: validate_ field
- Get the data of the field
- If the validation fails, throw an exception raise serializers.ValidationError('Check does not pass the description')
- Verify the pass and return the field data directly

```python
def validate_title(self, value):
    if "xx" in value:
        Raise serializers.ValidationError('This field contains the sensitive word')
    return value
```

#### Multi-field verification

- Define the validate method in the serializer
- attrs is a dictionary of all data
- Does not match throw exception exception serializers.ValidationError ('Checkout failed' instructions')

```python
def validate(self, attrs):
    # attrs is a dictionary composed of arrays
    if "linux" in attrs.get('title') and attrs['category_post'] == 2:
        return attrs
    else:
        Raise serializers.ValidationError('Library classification inconsistency')
```

#### Custom Validator

Use: Add validators=[custom validator,] in the field

```python
def my_validate(value):
    if "xxx" in value:
        Raise serializers.ValidationError('This field contains sensitive words!!')
    else:
        return value

# Serialization class
title = serializers.CharField(max_length=32, validators=[my_validate, ])
```

# Django Rest Framework components (4)

abstract

- Pagination
- view
- Routing
- Renderer
- django component: contenttype
  
## Source Analysis

N/a

## Pagination

### Functional Requirements

The following paging classes can be customized to inherit from the class, and then assign some variables for configuration.

- Pagination, see the nth page, display n data per page
  - from rest_framework.pagination import **PageNumberPagination**
- Pagination, n views backwards at n locations
  - from rest_framework.pagination import **LimitOffsetPagination**
- Encrypted paging, previous and next pages
  - from rest_framework.pagination import **CursorPagination**

```python
#序列化 - pager.py
from rest_framework import serializers
from api import models

class PagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = "__all__"

# views.py
from api.utils.serializers.pager import PagerSerializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class Pager1View(APIView):
    def get(self, request, *args, **kwargs):
        roles = models.Role.objects.all()
        #序列化1
        ser1 = PagerSerializer(instance=roles, many=True)

        #Execute pagination
        pg = PageNumberPagination()
        pager_roles = pg.paginate_queryset(queryset=roles, request=request, view=self)
        #序列化2
        ser2 = PagerSerializer(instance=pager_roles, many=True)

        # return Response(ser2.data)
        return pg.get_paginated_response(ser2.data)
```

## view

### Detailed explanation

- View (django.views)
- APIView (rest_framework.views)
  - Inherited View
- GenericAPIView (rest_framework.generics)
  - Inherit APIView
- GenericViewSet (rest_framework.viewsets)
  - Inherited ViewSetMixin
  - Inherited GenericAPIView
- （`过渡`）GenericViewSet、ListModelMixin、CreateModelMixin (rest_framework.viewsets / rest_framework.mixins)
- ModelViewSet (rest_framework.viewsets)
  - 继承mixins.CreateModelMixin
  - 继承mixins.RetrieveModelMixin
  - 继承mixins.UpdateModelMixin
  - 继承mixins.DestroyModelMixin
  - Inherit mixins.ListModelMixin
  - Inherited GenericViewSet

1. Role: (useless) view inherits GenericAPIView, then configure related properties, then call the relevant function to get the data!

```python
from api.utils.serializers.pager import PagerSerializer
from rest_framework.generics import GenericAPIView

class View1View(GenericAPIView):
    queryset = models.Role.objects.all()
    serializer_class = PagerSerializer
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):
        # retrieve data
        roles = self.get_queryset() # models.Role.objects.all()
        #值值
        pager_roles = self.paginate_queryset(roles)
        # Serialization
        ser = self.get_serializer(instance=pager_roles, many=True)
        return Response(ser.data)
```

Second, the role: the view inherits the GenericViewSet, and then implement the list and other methods!

```python
# urls.py
re_path('^(?P<version>[v1|v2|v3]+)/v1/$', views.View1View.as_view({'get': 'list'}))

# views.py
from api.utils.serializers.pager import PagerSerializer
from rest_framework.viewsets import GenericViewSet
class View1View(GenericViewSet):
    queryset = models.Role.objects.all()
    serializer_class = PagerSerializer
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        # retrieve data
        roles = self.get_queryset()
        #值值
        pager_roles = self.paginate_queryset(roles)
        # Serialization
        ser = self.get_serializer(instance=pager_roles, many=True)
        return Response(ser.data)
```

3. Role: (transition) view inherits ListModelMixin, CreateModelMixin and GenericViewSet, do not need to implement the list and other methods

```python
# urls.py
re_path('^(?P<version>[v1|v2|v3]+)/v1/(?P<pk>\d+)$', views.View1View.as_view({'get': 'list', 'post': 'create'}))

# views.py
from api.utils.serializers.pager import PagerSerializer
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin， CreateModelMixin
class View1View(ListModelMixin, CreateModelMixin、GenericViewSet):
    queryset = models.Role.objects.all()
    serializer_class = PagerSerializer
    pagination_class = PageNumberPagination
```

Role: The view inherits the ModelViewSet. Write the four lines of code as follows to complete the addition, deletion and change function!

```python
# urls.py
re_path('^(?P<version>[v1|v2|v3]+)/v1/(?P<pk>\d+)$', views.View1View.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update', 'patch': 'partial_update'}))

# views.py
from api.utils.serializers.pager import PagerSerializer
from rest_framework.viewsets import ModelViewSet
class View1View(ModelViewSet):
    queryset = models.Role.objects.all()
    serializer_class = PagerSerializer
    pagination_class = PageNumberPagination
```

### to sum up

- Write complex view code, recommended as follows
  - APIView
  - GenericViewSet
- If you only want to use basic additions, deletions, and changes: ModelViewSet
- If you only want to add or delete:
  - CreateModelMixin
  - DestroyModelMixin
  - GenericViewSet

## Routing

```python
from rest_framework import routers

# Automatically generate four commonly used URLs
router = routers.DefaultRouter()
Router.register(r'xx', view function)
Router.register(r'yy', view function)


urlpattern = [
    url(r'^', include(router.urls))
]
```

# Supplementary knowledge

1. Foreign key options for model classes (on_delete, realated_name)
2. Nested serialization of associated objects
   1. PrimaryKeyRelatedField
   2. Using the serializer class of the associated object
   3. StringRelatedField
3. DRF
   Serializer Serializer
   2. View base class
   3. Mixin extension class
   4. View set
   5. Routing Router
   6. Pagination / Exception Handling

## Defining options for foreign keys in a model class

### on_delete

- CASCADE cascading, when deleting the main table data, together with deleting the data in the foreign key table, this is a bit embarrassing, use with caution according to demand
- PROTECT protection, which prevents the deletion of data referenced by foreign keys in the primary table by throwing an exception ProtectedError exception
- SET_NULL is set to NULL, which means that when the main table deletes data, the table data associated with the foreign key is set to NULL, only if the field is null=True, and is allowed to be null.

### related_name

- When related_name is not used

```python
#一查多: One object. Multi-class name lowercase _set.all()
area = Area.objects.get(id=20000)
sub_areas = area.area_set.all()
```

- If using related_name

```python
# Set realted_name='subs'; when used, it is equivalent to changing the multi-class name lowercase _set to the subs set by related_name
sub_areas = area.subs.all()
```

## Nested serialization of associated objects

### PrimaryKeyRelatedField

Serialize the associated object to the primary key of the associated object

- When the read_only=True parameter is included, this field is only used for serialization
- When the queryset parameter is included, it will be used for parameter verification during deserialization

```python
Subs = PrimaryKeyRelatedField(label='lower level', read_only=True)
or:
Subs = PrimaryKeyRelatedField(label='lower area', queryset=Area.objects.all())
```

### Using serialized classes of associated objects

Serialize associated objects with the specified serializer

```python
Subs = AreaSerializer(label='lower level', many=True)
```

### StringRelatedField

Serialize the associated object to the string representation of the associated object (ie, the return value of the associated object model class __str__ method)

```python
Subs = serializers.StringRelatedField(label='lower level')
```

## Serialization & Deserialization

- Serialization: The process of converting a model object into a dictionary or JSON data
- Deserialization: The process of saving data passed to the front end to a model object

## Serializer - Serializer

### Features

Serialize and deserialize data

### Serializer definition

When using ModelSerializer

- Use model to specify model class
- Use fields to specify specific generated fields
- Use exclude to explicitly exclude which fields
- Use read_obly_fields to indicate read-only fields, ie fields for serialized output only
- Add or modify the original option parameters for the ModelSerializer using the extra_kwargs parameter

### Serialization function

Convert instance objects to dictionary data

- Serialize a single object
- Serialize multiple objects. (In fact, the addition of a parameter many=True on the basis of serializing a single object)
- Nested serialization of `associated objects'

note

- json.dumps() converts the dictionary to a json string
- json.loads() converts json strings to dictionary data

### Deserialization

- **Data verification**: We can call is_valid() to verify the data, we can also add ** additional verification**

```python
# 1. Write a function (such as about_django) to encapsulate the function of supplementary verification, then add the validators parameter to the field, as follows:
btitle = serializers.CharField(..., validators=[about_django])

# 2. Define a method validate_<field_name> in the serializer to verify the <field_name> field
def validate_btitle(self, value):
    ...
    return value

# 3. Define the validate method in the serializer for supplementary verification (combined with multiple field content verification)
def validate(self, attrs):
    # here attrs is a dictionary type of data, when the serializer object is created, the incoming data data
    ...
    return attrs
```

- **Data Save** (New & Update)

If you just pass in the data parameter when creating the serialized object, then the create method will be called to save the data; if the instance object is also passed in, the update method will be called to update the data.

Note: After the verification is passed, you need to call serializer.save() to save the data.

### save() and update() methods

- If after the verification is successful, you want to complete the creation of the data object based on validated_data, you can implement two methods: create() and update() in the **custom serialization class**.
  - def create(self, validated_data)
  - def update(self, instance, validated_data):
- If the serializer object is created, `the instance instance is not passed, then when the save() method is called, create() is called `, instead, `if the instance instance is passed, the save() method is called. Update() is called `
- Two notes:
  - When saving the serializer to save(), you can pass additional data, which can be obtained in the validated_data parameter in create() and update().
  - The default serializer must ** pass all required fields**, otherwise a validation exception will be thrown. But we can use the partial parameter to allow partial field updates (example one below)

```python
serializer = CommentSerializer(comment, data={'content': u'foo bar'}, partial=True)
```

```python
# Case 1: save()
from db.serializers import BookInfoSerializer
Data = {'btitle': 'Feng Shen Yan Yi'}
serializer = BookInfoSerializer(data=data)
serializer.is_valid()
Serializer.save() # <BookInfo: Fengshen's Romance > Object

# Case 2: update()
from db.models import BookInfo
book = BookInfo.objects.get(id=2)
Data = {'btitle': '依天剑'}
serializer = BookInfoSerializer(book, data=data)
serializer.is_valid()
Serializer.save() # <BookInfo: 依天剑> Object
```

### is_valid() method

Before getting the verified deserialized data, you must call the **is_valid()** method for validation (pass the dictionary to the data parameter, for example:

```python
data={}
s=Bookinfoserializer(data=data)
s.is_valid(raise_exception=True))
```

Valid returns True if the verification succeeds, otherwise returns False. If the verification is successful, the data can be obtained through the validated_data attribute of the serializer object.

- validate_<field_name> : check single field
- validate : Check multiple fields. After the other inspection methods are completed, this check will be done at the end.
- validators : supplemental checksum field

## View base class

### APIView

Is a subclass of the View class, adding some extra features based on the View class.

- The request object in the view is no longer the object of the original HttpRequest class in Django, but the object of the Request class encapsulated by the DRF framework.
  - **request.data**: The data of the request body after parsing is saved, and has been parsed into a dictionary or class dictionary, which is equivalent to the request.body/request.POST/request.FILES in the original request object of django.
  - **request.query_params**: Saves the data of the parsed string after parsing and has been parsed into a dictionary or class dictionary, equivalent to request.GET in django's original request object
- Can return the object of the Response class uniformly in response
  - Response class object: Incoming the original response data, it will automatically convert the response data to the corresponding format according to the client's request header. The default is json, only json and html are supported.
- Exception handling: If an unhandled exception is thrown in the view, the DRF framework will automatically handle the exception and will return the error message after processing to the client.
- Advanced Features
  - Certification
  - Permissions
  - Limiting

### GenericAPIView

Is a subclass of APIView, adding the method of "operation serializer" and `database query" on the basis of APIView

- Operation serializer
  - Attributes
    - serializer_class (specify the serializer class used by the view)
  - method
    - get_serializer_class returns the serializer class used by the view
    - get_serializer creates the serializer class object used by the view
- Database query
  - Attributes
    - queryset (specify the query set used by the view)
  - method
    - get_queryset returns the query set used by the view
    - get_object queries the specified object from the query set used by the view. The default query is based on pk.
- other functions
  - Filter
  - Classification

### Mixin extension class

The DRF framework provides five extension classes that encapsulate the process of universal additions and changes.

- **ListModelMixin**
  - Provides a list method that encapsulates a generic process for getting a set of data
- **CreateModelMixin**
  - Provides a create method that encapsulates a generic process for adding a new piece of data
- **RetrieveModelMixin**
  - Provides a retrieve method that encapsulates the generic process for getting the specified data
- **UpdateModelMixin**
  - Provides an update method that encapsulates the generic process for updating specified data
- **DestooryModelMixin**
  - Provides a destory method that encapsulates the generic process for deleting specified data

## View Set

In order to facilitate the development of RestAPI, the DRF framework provides some subclass view classes in addition to the APIView and GenericAPIView view classes. These subclass view classes inherit the GenericAPIView and the corresponding Mixin extension class, and provide corresponding request methods.

- view set parent class
  - GenericViewSet
  - ModelViewSet
  - ReadonlyModelViewSet
- the action attribute of the view set object

```python
def get_serializer_class(self):
    if self.action == 'list':
        ...
    elif self.action == 'latest':
        ...
    else:
        ...

def get_queryset(self):
    if self.action == 'list':
        ...
    elif self.action == 'latest':
        ...
    else:
        ...
```