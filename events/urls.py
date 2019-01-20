from django.urls import path
from events.views import *

app_name = 'events'

urlpatterns = [
    path('', EventCreateAPIView.as_view(), name="list"),
    path('<int:pk>/', EventDetailAPIView.as_view(), name="detail"),
]
