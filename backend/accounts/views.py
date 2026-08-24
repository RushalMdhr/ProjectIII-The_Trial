from django.shortcuts import render

# Create your views here.
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def test_connect(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            message = data.get("message", "")

            print("Message received from frontend:", message)

            return JsonResponse({
                "success": True,
                "message": f"Backend received: {message}"
            })

        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": str(e)
            }, status=400)

    return JsonResponse({
        "success": False,
        "message": "Only POST requests are allowed."
    }, status=405)