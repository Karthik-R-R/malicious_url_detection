
from django.db import models
from django.contrib.auth.models import User

class URLAnalysis(models.Model):
    url = models.URLField()
    probability = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):
    analysis = models.ForeignKey(URLAnalysis, on_delete=models.CASCADE)
    is_correct = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.analysis.url} by {self.user.username}"

class MLModel(models.Model):
    url = models.URLField(unique=True)
    prediction = models.CharField(max_length=100)
    analyzed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"MLModel for {self.url}"