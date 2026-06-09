from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
import requests
from .models import MediaServer
from .serializers import MediaServerSerializer

class MediaServerViewSet(viewsets.ModelViewSet):
    queryset = MediaServer.objects.all().order_by('-created_at')
    serializer_class = MediaServerSerializer

    @action(detail=True, methods=['post'])
    def test_connection(self, request, pk=None):
        server = self.get_object()
        try:
            url = server.base_url.rstrip('/')
            headers = {}
            if server.server_type == 'plex':
                url = f"{url}/identity"
                headers['X-Plex-Token'] = server.api_token
            elif server.server_type in ['emby', 'jellyfin']:
                url = f"{url}/System/Info/Public"
                headers['X-Emby-Token'] = server.api_token
            
            resp = requests.get(url, headers=headers, timeout=10, verify=False)
            if resp.status_code == 200:
                return Response({'status': 'success', 'message': 'Connection successful'})
            else:
                return Response({'status': 'error', 'message': f'Server responded with status {resp.status_code}'}, status=400)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=400)
