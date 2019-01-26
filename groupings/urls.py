from django.urls import path
from . import views
from django.conf.urls import url
from groupings.models import Grouping
from groupings.serializers import GroupingSerializer
from rest_framework.generics import ListCreateAPIView
app_name = 'groupings_api'
urlpatterns = [
    path('create/', views.create, name = 'create'),
    path('list/', views.GroupingListCreate.as_view()),
    path('list/<int:pk>/subscribe/', views.EventsSub.as_view()),
    path('list/saved/', views.GroupingListSavedCreate.as_view()),
    path('list/<int:pk>/', views.GroupingRetrieveDestroy.as_view()),
]