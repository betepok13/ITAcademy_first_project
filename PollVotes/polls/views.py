from django.http import HttpResponse, HttpRequest

__all__ = {'index'}


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Hello, World!')
