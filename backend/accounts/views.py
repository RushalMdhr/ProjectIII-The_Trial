from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def test_account(request):
    return Response({"message": "Account API is working!"})