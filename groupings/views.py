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
from rest_framework.response import Response

from .serializers import GroupingSerializer, MemeberSerializer, GroupingGetSerializer, GroupingSubSerializer

from .models import Grouping, Membership
from django.contrib.auth.models import User

from groupings.permission import IsMemberOnly, IsOwnerOnly
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


@api_view(["POST"])
@permission_classes((AllowAny, IsAuthenticated))
def create(request):
    print(request.data)
    grouping_serilializer = GroupingSerializer(data={"title": request.data["title"],
                                                     "description": request.data["description"],
                                                     "address": request.data["address"],
                                                     "price": request.data["price"],
                                                     "date": request.data["date"],
                                                     "time": request.data["time"],
                                                     "min_people": request.data["min_people"],
                                                     "type" : request.data["type"],
                                                     "city": request.data["city"],
                                                     "admin": request.user.pk})
    if grouping_serilializer.is_valid():
        print("ok")
        g = grouping_serilializer.save()
        return Response(
            grouping_serilializer.data
        , status=HTTP_200_OK)
    else:
        return Response(grouping_serilializer.errors, status=HTTP_400_BAD_REQUEST)


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
        return Grouping.objects.filter(members=self.request.user).latest('id')


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

#Duristap jiberu kerek
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


