from rest_framework import serializers
from .models import Document

class DocsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'description', 'file', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']
