from django.urls import path
from .views import *

urlpatterns = [
    path('message/board/', MessageBoardView.as_view(), name='messageboard'),
    path('subscribe', SubscribeView.as_view(), name='subscribe'),
    path('newsletter/', newsletter, name="newsletter"),


]
