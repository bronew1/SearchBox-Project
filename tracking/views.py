# tracking/views.py
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.timezone import now

@csrf_exempt
def track_event(request):
    if request.method == "POST":
        try:
            if request.body:
                data = json.loads(request.body)
            else:
                return JsonResponse({"error": "No request body"}, status=400)

            print("Event received:", data)
            return JsonResponse({"status": "ok"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid method"}, status=405)
