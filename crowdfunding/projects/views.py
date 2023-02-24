from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status, generics, permissions, filters

from django.db.models import Q
from itertools import chain

from .models import Project, Pledge, Comment, get_user_model
from .serializers import ProjectSerializer, PledgeSerializer, ProjectDetailSerializer, CommentSerializer, GlobalSearchSerializer 
from users.serializers import CustomUserSerializer
from users.models import CustomUser
from .permissions import IsOwnerOrReadOnly, IsSupporterOrReadOnly

from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.


''' Project list view '''

class ProjectList(generics.ListCreateAPIView):

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["is_open", "owner", "date_created"]
    search_fields = ["title", "description"]
    # can't have the same search fields and filter fields.

    def perform_create(self, serializer):
        serializer.save(supporter=self.request.user)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def get(self, request):
#         projects = Project.objects.all()
#         serializer = ProjectSerializer(projects, many=True)
#         return Response(serializer.data)
    
    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


''' Project detail view '''

class ProjectDetail(APIView):

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly
    ]

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
        return Response (status=status.HTTP_204_NO_CONTENT)


''' Pledge list view '''

class PledgeList(generics.ListCreateAPIView):

    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("supporter",)

    def perform_create(self, serializer):
        serializer.save(supporter=self.request.user)
    

    # Not needed for the filter to work
    # def get(self, request):
    #     pledges = self.filter_queryset(self.get_queryset)
    #     serializer = self.get_serializer(pledges, many = True)
    #     return Response(serializer.data)

class PledgeDetail(generics.RetrieveUpdateDestroyAPIView):
    
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsSupporterOrReadOnly
    ]

    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer


''' Comment list view '''
''' To be viewed in project list view/project detail view? '''

class CommentList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project',]
    
    def perform_create(self, serializer):
        serializer.save(commentator=self.request.user)
    
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
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

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
        return Response (status=status.HTTP_204_NO_CONTENT)


''' Global search view '''

# Modified from https://www.yeti.co/blog/global-search-in-django-rest-framework
class GlobalSearchList(generics.ListAPIView):   
    serializer_class = GlobalSearchSerializer   
    
    def get_queryset(self):      
        query = self.request.query_params.get('query', None)      
        projects = Project.objects.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(owner__username__icontains=query))


        users = CustomUser.objects.filter(Q
        (username__icontains=query) | Q
        (first_name__icontains=query) | Q
        (last_name__icontains=query) | Q
        (bio__icontains=query) | Q
        (country_of_residence__icontains=query) | Q
        (highest_level_of_education__icontains=query))

        all_results = [{"item": x, "type": str(type(x).__name__)} for x in chain(projects, users)]           
        return all_results
