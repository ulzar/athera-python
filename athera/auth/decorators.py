from functools import wraps
import jwt


def decorate_all_functions(function_decorator):
    def decorator(cls):
        for name, obj in vars(cls).items():
            if callable(obj):
                try:
                    obj = obj.__func__  # unwrap Python 2 unbound method
                except AttributeError:
                    pass  # not needed in Python 3
                setattr(cls, name, function_decorator(obj))
        return cls
    return decorator


def refresh_token_on_expiry(func):
    @wraps(func)
    def wrapper(*args, **kw):
        if func.__name__ == "__init__":
            return func(*args, **kw)
        self = args[0]  # the first element of args is the instanciated class
        if not hasattr(self, "oauth_client"):  # if it doesn't have this attribute, then we don't perform any check on the token
            return func(*args, **kw)
        access_token = self.token
        options = {  # The options defines what we want to verify. We only check for the token expiry.
            'verify_signature': False,
            'verify_exp': True,  # We want to check if the token is expired.
            'verify_nbf': False,
            'verify_iat': False,
            'verify_aud': False,
            'require_exp': True,  # We need the exp field in the token
            'require_iat': False,
            'require_nbf': False
        }
        try:
            _ = jwt.decode(access_token, '', options=options)
        except jwt.InvalidTokenError as err:
            try:
                token = self.oauth_client.refresh(access_token=self.token, refresh_token=self.refresh_token)
                if token:
                    self.token = token["access_token"]  # we refresh the attribute token of the class provided (self)
            except AttributeError:  # self.oauth_client may trigger AttributeError if the user does not want us to refresh the token automatically. In this case, we simply raise the jwt.InvalidTokenError error.
                raise err
        return func(*args, **kw)
    return wrapper
