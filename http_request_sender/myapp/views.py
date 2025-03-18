import requests
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.contrib.auth import authenticate

class LoginView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        request_data = request.data
        username = request_data.get("username", None)
        password = request_data.get("password", None)


        return Response({""})
class PostmanLikeAPIView(APIView):
    def post(self, request):
        url = request.data.get("url")
        method = request.data.get("method", "GET").upper()
        headers = request.data.get("headers", {})
        body = request.data.get("body", {})

        if isinstance(headers, str):
            try:
                headers = json.loads(headers)
            except json.JSONDecodeError:
                return Response({"error": "Invalid headers format"}, status=status.HTTP_400_BAD_REQUEST)

        if isinstance(body, str):
            try:
                body = json.loads(body)
            except json.JSONDecodeError:
                return Response({"error": "Invalid body format"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            response = None
            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                response = requests.post(url, json=body, headers=headers)
            elif method == "PUT":
                response = requests.put(url, json=body, headers=headers)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers)
            else:
                return Response({"error": "Invalid HTTP method"}, status=status.HTTP_400_BAD_REQUEST)

            print("response::",response)

            return Response({
                "status": response.status_code,
                "response": response.json() if response.text else "No Response"
            }, status=status.HTTP_200_OK)

        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

