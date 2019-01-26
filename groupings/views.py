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
@permission_classes((AllowAny,))
def create(request):
    """
    post:
    create groupings with list of members by list of user's pk

    """

    print(request.data)
    grouping_serilializer = GroupingSerializer(data={"title": request.data["title"], "admin": request.user.pk})
    if grouping_serilializer.is_valid():
        print("ok")
        g = grouping_serilializer.save()
        # for i in request.data['members_all']:
        #     try:
        #         user = User.objects.get(pk=i)
        #         check = Membership.objects.filter(user=user, grouping=g)
        #         print(check)
        #         if len(check) == 0:
        #             Membership.objects.create(user=user, grouping=g)
        #     except User.DoesNotExist:
        #         return Response("User does not exist", status=HTTP_400_BAD_REQUEST)
        # user = User.objects.get(pk=request.user.pk)
        # Membership.objects.create(user=user, grouping=g)
        return Response({
            'smallevents': grouping_serilializer.data
        }, status=HTTP_200_OK)
    else:
        print("not ok")
        return Response(grouping_serilializer.errors, status=HTTP_400_BAD_REQUEST)


class GroupingListCreate(generics.ListCreateAPIView):
    """
    provide all groups of person

    """
    # queryset = Grouping.objects.all()
    serializer_class = GroupingGetSerializer
    permission_classes = (IsMemberOnly, IsAuthenticated)
    print("1")

    def get_queryset(self):
        print("2")
        user = self.request.user
        #return Grouping.objects.filter(members=self.request.user)
        return Grouping.objects.all()

    # def list(self,request):
    #     groupings = request.user.grouping_set
    #     groupings_serializer = GroupingSerializer(groupings, many = True)
    #     return Response(groupings_serializer.data)

class GroupingListSavedCreate(generics.ListCreateAPIView):
    serializer_class =  GroupingGetSerializer
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
    serializer_class = GroupingSubSerializer

    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.user.pk)
        # grouping_serilializer = Grouping.objects.filter(title=self.kwargs['id'])
        grouping_serilializer = Grouping.objects.get(id=self.kwargs['pk'])
        Membership.objects.update_or_create(user=user, grouping=grouping_serilializer)
        return Response({'OK'}, status=HTTP_200_OK)


    # def get(self, request, id, **kwargs):
    #     user = User.objects.get(,
    #     grouping_serilializer = Grouping.objects.filter(id=id)
    #     Membership.objects.create(user=user, grouping=grouping_serilializer)



