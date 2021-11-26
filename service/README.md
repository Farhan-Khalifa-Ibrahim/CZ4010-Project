## Service Classes

This class contains classes that makes HTTP requests.

## `AuthService`

This class calls Firebase Authentication using REST API to login or create a new account.

### Creating Account

Call the `sign_up` method and pass in the email and password. If creation is successful, the user's `uid` will be returned.

> ⚠️ Password must be at least 6 characters. This rule is imposed by Firebase Authentication.

```python
auth = AuthService()
uid = auth.sign_up(email, password)
```

### Logging in

Call the `sign_in` method and pass in the email and password. If login is successful, the user's `uid` will be returned.

```python
auth = AuthService()
uid = auth.sign_in(email, password)
```
