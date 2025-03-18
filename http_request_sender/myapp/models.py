from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(max_length=70, unique=True, null=True, default=None)
    username = models.CharField(max_length=100, unique=True, null=True, default=None)
    first_name = models.CharField(max_length=100, null=True, default=None)
    last_name = models.CharField(max_length=100, null=True, default=None)
    is_premium = models.BooleanField(default=False)
    subscription_expiry = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.email if self.email else self.username
    
class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="collections")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class APIRequest(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="requests")
    name = models.CharField(max_length=255)
    method = models.CharField(max_length=10, choices=[("GET", "GET"), ("POST", "POST"), ("PUT", "PUT"), ("DELETE", "DELETE")])
    url = models.URLField()
    headers = models.JSONField(default=dict, blank=True)
    body = models.JSONField(default=dict, blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    version = models.PositiveIntegerField(default=1) 

    def save(self, *args, **kwargs):
        if self.pk:
            self.version += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.method} {self.url} (v{self.version})"

class APIRequestHistory(models.Model):
    api_request = models.ForeignKey(APIRequest, on_delete=models.CASCADE, related_name="history")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    executed_at = models.DateTimeField(auto_now_add=True)
    response_status = models.PositiveIntegerField()  # HTTP Status Code
    response_body = models.JSONField(default=dict, blank=True, null=True)
    headers_sent = models.JSONField(default=dict, blank=True)
    body_sent = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.api_request.name} @ {self.executed_at}"
