from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'completed', 'created_at', 'image']

    def validate_image(self, value):
        if value:
            if value.size > 1024 * 1024 * 200:  # 8Kの時用に200MBの制約に変更
                raise serializers.ValidationError("画像サイズは200MB以下にしてください。")
            if not value.content_type.startswith('image/'):
                raise serializers.ValidationError("アップロードできるのは画像ファイルのみです。")
        return value