from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Posts
from .models import Users
from .serializers import PostSerializer
from .serializers import UsersSerializer
from django.core.urlresolvers import resolve
from django.utils.encoding import smart_str
from django.http import FileResponse, HttpResponse
import os


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


def get_post(request):
    if request.method == 'GET':
        file_name = request.path_info.split('/', 3)[-1]
        file_path = os.path.join('_static', 'pdfs', file_name)
        print 'Downloading...', file_name
        response = HttpResponse(open(file_path, 'rb').read())
        response['Content-Type'] = 'mimetype/submimetype'
        response['Content-Disposition'] = 'attachment; filename=%s' % file_name
        return response
