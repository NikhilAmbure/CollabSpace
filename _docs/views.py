from django.shortcuts import render
from .serializers import DocsSerializer
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response


class DocsViewSet(viewsets.ModelViewSet):
    serializer_class = DocsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Document.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Return the 5 most recent documents of the user"""
        recent_docs = self.get_queryset().order_by('-uploaded_at')[:5]
        serializer = self.get_serializer(recent_docs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search documents by title (case-insensitive)"""
        query = request.query_params.get('q', '')
        docs = self.get_queryset().filter(title__icontains=query)
        serializer = self.get_serializer(docs, many=True)
        return Response(serializer.data)
        