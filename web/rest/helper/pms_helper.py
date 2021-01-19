from flask import request
from functools import wraps

# checking rquired filds
def pms_validation(func):
    @wraps(func)
    def warp (*args, **kwargs):
        data = request.get_json()
        required = ['url', 'username', 'password']
        if not all(field in data for field in required):
            return 'Missing values '+" or ".join(required), 400
        else:
            return func(*args, **kwargs)
    return warp

