from models import Post
from rest_framework import serializers


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        # fields = ('postid', 'userid', 'title', 'body')
        fields = '__all__'
