import os

import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from websock import routing as websock_routing
from multiplechat import routing as multiple_routing
from django_channels_jwt_auth_middleware.auth import JWTAuthMiddlewareStack


from channels.sessions import SessionMiddlewareStack
from channels.security.websocket import OriginValidator, AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agentmain.settings')
django.setup()
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': SessionMiddlewareStack(
        JWTAuthMiddlewareStack(
            URLRouter(
                websock_routing.websocket_urlpatterns+
                multiple_routing.websocket_urlpatterns
            )
        ),
    )

})
