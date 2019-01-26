from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from events.models import Events
from events.permissions import UserIsOwnerEvents
from events.serializers import EventSerializer


class EventCreateAPIView(ListCreateAPIView):
    serializer_class = EventSerializer


    def get_queryset(self):
        return Events.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EventDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    queryset = Events.objects.all()
    permission_classes = (IsAuthenticated, UserIsOwnerEvents)

