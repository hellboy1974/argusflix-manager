import re

with open("core/api_views.py", "r", encoding="utf-8") as f:
    content = f.read()

new_endpoints = """
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_active_connections(request):
    try:
        from core.utils import RedisClient
        import json
        rc = RedisClient()
        connections = []
        keys = rc.keys("stream:connection:*")
        for key in keys:
            data = rc.get(key)
            if data:
                try:
                    conn = json.loads(data)
                    connections.append(conn)
                except Exception:
                    pass
        return Response(connections)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def kill_active_connection(request, client_id):
    try:
        from core.utils import RedisClient
        rc = RedisClient()
        
        # Kill logic: We can signal the client to stop
        rc.set(f"stream:stop:{client_id}", "true", 300)
        
        # Also clean up connection key
        keys = rc.keys(f"stream:connection:*:{client_id}")
        for key in keys:
            rc.delete(key)
            
        return Response({"success": True})
    except Exception as e:
        return Response({"error": str(e)}, status=500)
"""

content = content + new_endpoints

with open("core/api_views.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Patched core/api_views.py!")
