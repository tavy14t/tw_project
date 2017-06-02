from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Posts
from .models import Users
from .serializers import PostSerializer
from .serializers import UsersSerializer


class PostList(APIView):
    def get(self, request):
        posts = Posts.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        pass


class UsersList(APIView):
    def get(self, request):
        users = Users.objects.all()
        serializer = UsersSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        pass
