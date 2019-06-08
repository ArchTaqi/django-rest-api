# Django

# Working with JWT For API Authentication in Django

- JSON web token is a useful way for you to  provide valid users access to your API endpoints without the need to add a access token.
- Which could solve your headaches in integrating authentication for your REST API to prevent unknown hackers in accessing your API endpoints.
- Due to it's simplicity and it does not require the use of database to store your tokens.
- It is a quickway for your django backend to provide REST API endpoints tokens to interact with a web front-end technology like React, Vue or Angular without the use of OAuth.

## DRF Views

1. APIViews
2. ViewSet

### 1. APIView

> API view is the most basic type of view, it enables us to describe the logic which makes our API endpoint.

- Perfect for implementing complex logic i.e calling other apis and local files.
- Need full control over logic


### 2. ViewSet

- Perfect for standard database operations, fastest way to make database interactions.
- Used when needed CRUD, no customize and complex logic.

