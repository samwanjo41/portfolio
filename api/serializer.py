from rest_framework import serializers
from core.models import Project

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['title', 'description', 'image', 'main_language', 'premium', 'url_link']

    