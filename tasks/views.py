from django.shortcuts import render
from .models import Task
from .serializers import TaskSerializer
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Only return tasks owned by the current logged-in user
        return Task.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically assign the logged-in user as owner
        serializer.save(owner=self.request.user)
        
    @action(detail=False, methods=['get'])
    def completed(self, request):
        """Returns only completed tasks of logged-in user"""
        completed_tasks = self.get_queryset().filter(is_completed=True)
        serializer = self.get_serializer(completed_tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        pending_tasks = self.get_queryset().filter(is_completed=False)
        serializer = self.get_serializer(pending_tasks, many=True)
        return Response(serializer.data)