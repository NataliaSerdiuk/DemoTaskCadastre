from django.urls import path
from .views import query, send_request_to_external_service, history, get_result, ping

urlpatterns = [
    path('query/', query, name='query'),
    # path('result/', send_request_to_external_service, name='send'),
    path('result/', get_result, name='result'),
    path('history/', history, name='history'),
    path('ping/', ping, name='ping'),
]