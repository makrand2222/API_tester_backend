from django.urls import path
from .views import PostmanLikeAPIView

urlpatterns = [
    path("postman/", PostmanLikeAPIView.as_view(), name="postman_view"),
]
