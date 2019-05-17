from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED,
)
from rest_framework import status as sts

from rest_framework.response import Response

from .serializers import GroupingSerializer, MemeberSerializer, GroupingGetSerializer, GroupingSubSerializer, \
    SmallEventCreatingSerializer

from .models import Grouping, Membership, Coordinate
from django.contrib.auth.models import User

from groupings.permission import IsMemberOnly, IsOwnerOnly
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def create(request):
    global sevent
    sevent_serilizer = SmallEventCreatingSerializer(data=request.data)
    if sevent_serilizer.is_valid():
        coor = Coordinate.objects.create(latitude=request.data["coordinates"]["latitude"],
                                         longitude=request.data["coordinates"]["longitude"])
        sevent = \
            Grouping.objects.create(coordinates=coor,
                                    title=sevent_serilizer.validated_data["title"],
                                    address=sevent_serilizer.validated_data["address"],
                                    city=sevent_serilizer.validated_data["city"],
                                    date=sevent_serilizer.validated_data["date"],
                                    description=sevent_serilizer.validated_data["description"],
                                    min_people=sevent_serilizer.validated_data["min_people"],
                                    price=sevent_serilizer.validated_data["price"],
                                    time=sevent_serilizer.validated_data["time"],
                                    type=sevent_serilizer.validated_data["type"],
                                    admin_id=request.user.id
                                    )
        return Response(
            data=SmallEventCreatingSerializer(sevent).data,
            status=HTTP_200_OK
        )
    else:
        return Response(
            data=sevent_serilizer.errors,
            status=HTTP_400_BAD_REQUEST
        )


class GroupingListCreate(generics.ListCreateAPIView):
    serializer_class = GroupingGetSerializer
    permission_classes = (IsMemberOnly, IsAuthenticated)
    print("1")

    def get_queryset(self):
        user = self.request.user
        # return Grouping.objects.all()
        return Grouping.objects.exclude(members=self.request.user)


class GroupingListSavedCreate(generics.ListCreateAPIView):
    serializer_class = GroupingGetSerializer
    permission_classes = (IsMemberOnly, IsAuthenticated)

    def get_queryset(self):
        user = self.request.user
        return Grouping.objects.filter(members=self.request.user)


class GroupingRetrieveDestroy(generics.RetrieveDestroyAPIView):
    permission_classes = [IsMemberOnly, IsAuthenticated]
    queryset = Grouping.objects.all()
    serializer_class = GroupingGetSerializer


class EventsSub(generics.RetrieveUpdateAPIView):
    permission_classes = [IsMemberOnly, IsAuthenticated]
    queryset = Grouping.objects.all()
    serializer_class = GroupingGetSerializer

    def get_queryset(self):
        print(self.request.data)
        # print(self)
        user = User.objects.get(pk=self.request.user.pk)
        # grouping_serilializer = Grouping.objects.filter(title=self.kwargs['id'])
        grouping_serilializer = Grouping.objects.get(id=self.kwargs['pk'])
        Membership.objects.update_or_create(user=user, grouping=grouping_serilializer)
        return Grouping.objects.filter(members=self.request.user)


# Duristap jiberu kerek
class EventsUnSub(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Grouping.objects.all()
    serializer_class = GroupingGetSerializer

    def get_queryset(self):
        user = User.objects.get(pk=self.request.user.pk)
        # grouping_serilializer = Grouping.objects.filter(title=self.kwargs['id'])
        grouping_serilializer = Grouping.objects.get(id=self.kwargs['pk'])
        mem = Membership.objects.get(user=user, grouping=grouping_serilializer)
        mem_ext = Membership.objects.filter(user=user, grouping=grouping_serilializer).exists()
        print(Grouping.objects.get(id=self.kwargs['pk']))
        mem.delete()
        return Grouping.objects.filter(title=grouping_serilializer)
