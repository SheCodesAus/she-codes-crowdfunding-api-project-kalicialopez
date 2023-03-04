from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status, generics, permissions, filters

from django.db.models import Q
from itertools import chain

from .models import Project, Pledge, Comment, get_user_model
from .serializers import (
    ProjectSerializer, 
    PledgeSerializer,
    PledgeDetailSerializer, 
    ProjectDetailSerializer, 
    CommentSerializer, 
    GlobalSearchSerializer
    )

from users.serializers import CustomUserSerializer
from users.models import CustomUser
from .permissions import (
    IsOwnerOrReadOnly, 
    IsSupporterOrReadOnly,
    IsCommentatorOrReadOnly
    )

from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.


''' Project list view '''


class ProjectList(generics.ListCreateAPIView):

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["is_open", "owner", "date_created", "campaign_deadline",  "educational_institution",
                        "current_occupation_or_industry", "desired_occupation_or_industry"]
    search_fields = ["title", "description"]
    # can't have the same search fields and filter fields.

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, supporter=self.request.user, )

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     experimental code
#     def get(self, request):
#         projects = Project.objects.all()
#         serializer = ProjectSerializer(projects, many=True)
#         return Response(serializer.data)

# Don't really need a post in the listview?
    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


''' Project detail view '''


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, 
        IsOwnerOrReadOnly
    ]
    serializer_class = ProjectDetailSerializer

# The following functions may be useless due to changing from APIView to generics.RetrieveUpdateDestroyAPIView?

    def get_object(self, pk):
        try:
            project = Project.objects.get(pk=pk)
            self.check_object_permissions(self.request, project)
            return project
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk):
        project = self.get_object(pk)
        data = request.data
        serializer = ProjectDetailSerializer(
            instance=project,
            data=data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # https://www.youtube.com/watch?v=b680A5fteEo
    def delete(self, request, pk):
        project = self.get_object(pk=pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


''' Pledge list view '''


class PledgeList(generics.ListCreateAPIView):

    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("supporter", "project")

    def perform_create(self, serializer):
        serializer.save(supporter=self.request.user)

    # Not needed for the filter to work
    # def get(self, request):
    #     pledges = self.filter_queryset(self.get_queryset)
    #     serializer = self.get_serializer(pledges, many = True)
    #     return Response(serializer.data)


class PledgeDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, 
        IsSupporterOrReadOnly
    ]
    queryset = Pledge.objects.all()
    serializer_class = PledgeDetailSerializer

# Experimental code (copied from ProjectDetailView) The following functions may be useless seeing as this was always a generics.ReRetrieveUpdateDestroyAPIView

    def get_object(self, pk):
        try:
            pledge = Pledge.objects.get(pk=pk)
            self.check_object_permissions(self.request, pledge)
            return pledge
        except Pledge.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        pledge = self.get_object(pk)
        serializer = PledgeDetailSerializer(pledge)
        return Response(serializer.data)

    def put(self, request, pk):
        pledge = self.get_object(pk)
        data = request.data
        serializer = PledgeDetailSerializer(
            instance=pledge,
            data=data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # https://www.youtube.com/watch?v=b680A5fteEo
    def delete(self, request, pk):
        pledge = self.get_object(pk=pk)
        pledge.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


''' Comment list view '''
''' To be viewed in project list view/project detail view on front-end '''


class CommentList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project', ]

    def perform_create(self, serializer):
        serializer.save(commentator=self.request.user)
    
    # Experimental code - trying to link up the comment owner to the project with Ben Derham (mentor)
    # def get(self, request, project_pk):
    #     project = Project.objects.get(pk=project_pk)
    #     comments = CommentList.objects.filter(project=project)
    #     comment_serializer = CommentSerializer(comments, many=True)

    #     return Response({
    #         'comments': comment_serializer.data
    #     })

    # the above def get is based off this code 
    # def get(self, request, country_pk):
    #     # get the country by its primary key from the url
    #     country = Country.objects.get(pk=country_pk)

    #     locations = Location.objects.filter(country=country)
    #     location_serializer = LocationSerializer(locations, many=True)

    #     return Response({
    #         'locations': location_serializer.data
    #     })

    # Experimental code, may be useless?
    # def post(self, request):
    #     serializer = CommentSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(
    #             serializer.data,
    #             status=status.HTTP_201_CREATED
    #         )
    #     return Response(
    #         serializer.errors,
    #         status=status.HTTP_400_BAD_REQUEST
    #     )


''' Comment Detail View '''
''' Logged in user is currently unable to edit comments. Unsure if this is because I do not have a CommentDetailSerializer? '''


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsCommentatorOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


# Experimental code, may be useless due to this being a generics.RetrieveUpdateDestroyAPIView?
    def get_object(self, pk):
        try:
            comment = Comment.objects.get(pk=pk)
            self.check_object_permissions(self.request, comment)
            return comment
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, pk):
        comment = self.get_object(pk)
        data = request.data
        serializer = CommentSerializer(
            instance=comment,
            data=data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comment = self.get_object(pk=pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


''' Global search view '''

# Modified from https://www.yeti.co/blog/global-search-in-django-rest-framework


class GlobalSearchList(generics.ListAPIView):
    serializer_class = GlobalSearchSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', None)
        projects = Project.objects.filter(Q
                                          (title__icontains=query) | Q
                                          (description__icontains=query) | Q
                                          (course_name__icontains=query) | Q
                                          (educational_institution__icontains=query) | Q
                                          (current_occupation_or_industry__icontains=query) | Q
                                          (desired_occupation_or_industry__icontains=query) | Q
                                          (owner__username__icontains=query))

        users = CustomUser.objects.filter(Q
                                          (username__icontains=query) | Q
                                          (first_name__icontains=query) | Q
                                          (last_name__icontains=query) | Q
                                          (bio__icontains=query) | Q
                                          (country_of_residence__icontains=query) | Q
                                          (highest_level_of_education__icontains=query))

        all_results = [{"item": x, "type": str(
            type(x).__name__)} for x in chain(projects, users)]
        return all_results
