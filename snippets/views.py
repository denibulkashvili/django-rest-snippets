"""Creates snippets views"""
from rest_framework import generics
from rest_framework import permissions

from snippets.permissions import IsOwnerOrReadOnly

from django.contrib.auth.models import User

from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer


# Create your views here.

class SnippetViewSet(viewsets.ModelViewSet):
    """Snippet class that provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    Additionally custom action `highlight` is created"""
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)
    
    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer]) # create custom action
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Creates User viewset with automatically provided `list` and `detail` actions"""
    queryset = User.objects.all()
    serializer_class = UserSerializer



@api_view(['GET'])
def api_root(request, format=None):
    """Creates single entry point to API"""
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format),
    })