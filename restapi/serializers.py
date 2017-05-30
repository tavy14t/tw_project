from models import Posts
from models import Users
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ('title', 'body')


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('firstname', 'lastname', 'email')
