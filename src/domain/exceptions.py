class BaseError(Exception):
    status_code = 500
    pass


class DomainError(BaseError):
    status_code = 400
    pass


class AuthError(BaseError):
    status_code = 401
    pass
