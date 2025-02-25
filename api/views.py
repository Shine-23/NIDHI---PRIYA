from rest_framework.views import APIView
from api.bigquery_client import query_with_retry
from .metrics import log_request, set_primary_status, get_metrics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

import os
from django.http import JsonResponse


class CustomerListView(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication

    def get(self, request):
        if not request.user.is_staff:  # Only admins can access
            return JsonResponse({"error": "Access denied. Admins only."}, status=403)

        # Fetch customer data as usual
        log_request("primary")
        query = "SELECT * FROM `dsd-proj-444318.ecommerce_dataset.Customer` LIMIT 100"
        data = query_with_retry(query)
        if data:
            return JsonResponse(data, safe=False)
        return JsonResponse({"error": "Failed to fetch customer data"}, status=500)

class ProductListView(APIView):
    def get(self, request):
        log_request("primary")  # Log the request
        query = "SELECT * FROM `dsd-proj-444318.ecommerce_dataset.Product` LIMIT 100"
        data = query_with_retry(query)
        if data:
            return Response(data)
        else:
            return Response({"error": "Failed to fetch product data"}, status=500)

class TransactionListView(APIView):
    def get(self, request):
        log_request("primary")  # Log the request
        query = "SELECT * FROM `dsd-proj-444318.ecommerce_dataset.Transactions` LIMIT 100"
        data = query_with_retry(query)
        if data:
            return Response(data)
        else:
            return Response({"error": "Failed to fetch transaction data"}, status=500)

class ClickStreamListView(APIView):
    def get(self, request):
        log_request("primary")  # Log the request
        query = "SELECT * FROM `dsd-proj-444318.ecommerce_dataset.Click_Stream` LIMIT 100"
        data = query_with_retry(query)
        if data:
            return Response(data)
        else:
            return Response({"error": "Failed to fetch transaction data"}, status=500)
        
def shutdown_service(request):
    try:
        # Find the process using port 8000
        result = os.popen('netstat -ano | findstr :8000').read()
        lines = result.strip().split('\n')
        for line in lines:
            if "LISTENING" in line:
                pid = line.split()[-1]  # Extract the PID (last column)
                os.system(f"taskkill /F /PID {pid}")  # Kill the specific process
                return JsonResponse({"message": "Service on port 8000 stopped successfully"})

        return JsonResponse({"error": "No service found on port 8000"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def metrics_view(request):
    return JsonResponse(get_metrics())

def log_request_view(request):
    request_type = request.GET.get("type", None)
    if request_type:
        log_request(request_type)
        return JsonResponse({"message": f"{request_type} request logged successfully."})
    return JsonResponse({"error": "Request type not specified."}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def secure_data(request):
    if request.user.is_staff:  # Check if the user is an admin
        return JsonResponse({"data": "This is secure admin data."})
    return JsonResponse({"error": "Access denied. Admins only."}, status=403)
