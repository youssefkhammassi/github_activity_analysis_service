import logging

from fastapi import HTTPException
from starlette import status


class UnprocessableEntity(HTTPException):
    """*422* unprocessable entity`
    Raise if there was an error while validating data
    """
    def __init__(self, detail):
        logging.error(detail)
        super().__init__(detail=detail, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    description = (
        "The browser (or proxy) sent a request that this server could "
        "not understand."
    )


class BadRequest(HTTPException):
    """*400* `Bad Request`
    Raise if the browser sends something to the application
    or the server which they cannot handle.
    """

    def __init__(self, detail):
        logging.error(detail)
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST)

    description = (
        "The browser (or proxy) sent a request that this server could "
        "not understand."
    )


class NotFoundException(HTTPException):
    """*404* `Not found`
    Raise if the browser sends something to the application
    or the server which they cannot find.
    """

    def __init__(self, detail):
        logging.error(detail)
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)


class InternalError(HTTPException):
    """*500* `Internal Server Error`
    Raise if an internal server error occurred.  This is a good fallback if an
    unknown error occurred in the dispatcher.
    """

    def __init__(self, detail):
        logging.error(detail)
        super().__init__(detail=detail, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ApiNotValidGithubURL(BadRequest):
    def __init__(self, detail):
        super().__init__(detail=detail)
