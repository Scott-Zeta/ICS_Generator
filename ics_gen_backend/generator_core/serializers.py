from rest_framework import serializers
from PIL import Image

class PostSerializer(serializers.Serializer):
    text = serializers.CharField(required=False, allow_blank=True, max_length=500, trim_whitespace=True)
    
    image = serializers.ImageField(required=False, allow_empty_file=True, max_length=50, use_url=False)
    
    def validate(self,data):
        if not data.get('text') and not data.get('image'):
            raise serializers.ValidationError("Both text and image can not be empty")
        return data
    
    def validate_image(self, value):
        if value:
            if value.size > 5 * 1024*1024:
                raise serializers.ValidationError("File can not larger than 5MB")
            
            try:
                img = Image.open(value)
                if not value.image.format.lower() in ['jpg','jpeg','png','webp','svg','gif']:
                    raise serializers.ValidationError("File format not supported")
            except Exception:
                raise serializers.ValidationError("File is not a valid image")
            
            img.close()
        return value