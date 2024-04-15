from rest_framework import serializers

class PostSerializer(serializers.Serializer):
    text = serializers.CharField(required=False, allow_blank=True, max_length=500, trim_whitespace=True)
    