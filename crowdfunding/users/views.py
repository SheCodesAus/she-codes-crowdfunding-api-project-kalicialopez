from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from users.models import CustomUser
from .serializers import CustomUserSerializer, ChangePasswordSerializer
from .permissions import IsUserOrReadOnly

# Create your views here.

class CustomUserList(APIView):

    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class CustomUserDetail(APIView):

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsUserOrReadOnly
    ]
    
    def get_object(self, pk):
        try:
            instance =  CustomUser.objects.get(pk=pk)
            self.check_object_permissions(self.request, instance)
            return instance
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        data = request.data
        serializer = CustomUserSerializer(
            instance=user,
            data=data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
  # edit user detail not working.  


class SessionUserDetailView(APIView):

    permission_classes = [
        permissions.IsAuthenticated]
    
    def get_object(self):
        try:
            return self.request.user
        except CustomUser.DoesNotExist:
            raise Http404
    def get(self, request):
        print(request)
        user = self.get_object()
        serializer = CustomUserSerializer(user)
        return Response(serializer.data) 

class ChangePasswordView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer