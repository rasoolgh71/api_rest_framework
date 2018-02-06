from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,Http404
#from django.views.decorators.csrf import csrf_exempt,
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from api.serializers import SnippetSerializer
from api.serializers import UserSerializer
from rest_framework.decorators import api_view,APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework.reverse import reverse
# Create your views here.
class  IsOwnerOrReadOnly(permissions.BasePermission):
    """"
    class permition only allow owewr login
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner==request.user

class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer)
    def get(self,request,*args,**kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

class SnippetList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SnippetDetail(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
     queryset = Snippet.objects.all()
     serializer_class = SnippetSerializer
     permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)

     def get(self,request,*args,**kwargs):
       return self.retrieve(request,*args,**kwargs)

     def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

     def delete(self,request,*args,**kwargs):
         return self.destroy(request,*args,**kwargs)



class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset =  User.objects.all()
    serializer_class = UserSerializer
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })
