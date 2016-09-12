from .settings import WS_HOST


def ws_host(request):
    if WS_HOST:
        return {'ws_host': WS_HOST}
    else:
        return {'ws_host': False}
