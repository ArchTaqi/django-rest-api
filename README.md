# Django REST APIs with DRF

An example RESTful API built using Django 2.2

## Best Practices for Designing a Pragmatic RESTful API

    Use RESTful URLs and actions
    Version via the URL, not via headers
    HATEOAS
    Use query parameters for advanced filtering, sorting & searching
    Limit which fields are returned from the API
    Return something useful from POST, PATCH & PUT requests
    Pretty print by default & gzip supported
    Consider using JSON for POST, PUT and PATCH request bodies
    Paginate using Link headers
    Use token based authentication
    Include response headers that facilitate caching
    Effectively use HTTP Status codes
    
# Pet Store

### Pet

### Store

### User


# Testing

**_Token Creation_**

In case of new user 
```bash
`$ http POST 127.0.0.1:8000/api-register/ username=muhammadtaqi password=Yourpass! email=taqi.official@gmail.com`
```
return an confirmation URL
```json
{
    "confirmation_url": "http://127.0.0.1:8000/api-activate/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImtyenlzenRvZkBrei5jb20iLCJ1c2VyX2lkIjoyNSwidXNlcm5hbWUiOiJrcnp5c2llayIsImV4cCI6MTQ3OTA1MDQ5M30.CMcW8ZtU6AS9LfVvO-PoLyqcwi6cOK1VzI2o7pEPX2k/"
}
```

```bash
$ http GET http://127.0.0.1:8000/api-activate/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImtyenlzenRvZkBrei5jb20iLCJ1c2VyX2lkIjoyNSwidXNlcm5hbWUiOiJrcnp5c2llayIsImV4cCI6MTQ3OTA1MDQ5M30.CMcW8ZtU6AS9LfVvO-PoLyqcwi6cOK1VzI2o7pEPX2k/
```
```json
[
    "User Activated"
]
```
Login with Your Creds now.....
```bash
$ http POST 127.0.0.1:8000/api-auth/ username=muhammadtaqi password=Yourpass!
```
```json
{
    "token": "<JWT-TOKEN>"
}
```
```bash
$ http POST 127.0.0.1:8000/api/v1/pets/ 'Authorization: Bearer <jwt-token>'
```

**_Token Verification_**

`$ http POST 127.0.0.1:8000/token-verify/ token=<jwt-token>`

**_Token Refresh_**

`$ http POST 127.0.0.1:8000/token-refresh/ token=<existing-jwt-token>`

## Environment variables

These are common between environments. The `ENVIRONMENT` variable loads the correct settings, possible values are: `DEVELOPMENT`, `STAGING`, `PRODUCTION`.

```
ENVIRONMENT='DEVELOPMENT'
DJANGO_SECRET_KEY='dont-tell-eve'
DJANGO_DEBUG='yes'
```

These settings(and their default values) are only used on staging and production environments.

```
DJANGO_SESSION_COOKIE_SECURE='yes'
DJANGO_SECURE_BROWSER_XSS_FILTER='yes'
DJANGO_SECURE_CONTENT_TYPE_NOSNIFF='yes'
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS='yes'
DJANGO_SECURE_HSTS_SECONDS=31536000
DJANGO_SECURE_REDIRECT_EXEMPT=''
DJANGO_SECURE_SSL_HOST=''
DJANGO_SECURE_SSL_REDIRECT='yes'
DJANGO_SECURE_PROXY_SSL_HEADER='HTTP_X_FORWARDED_PROTO,https'
```

### Heroku

```bash
$ heroku create
$ heroku addons:add heroku-postgresql:hobby-dev
$ heroku pg:promote DATABASE_URL
$ heroku config:set ENVIRONMENT=PRODUCTION
$ heroku config:set DJANGO_SECRET_KEY=`./manage.py generate_secret_key`
```

## REsources

- [Django Builder](http://mmcardle.github.io/django_builder/#!/models)
- [Django, Docker and Postgres](https://wsvincent.com/django-docker-postgresql)