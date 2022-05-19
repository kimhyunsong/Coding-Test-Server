from django.db import models

# Create your models here.
class Problem(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    answer = models.TextField()

class Solution(models.Model):
    user = models.CharField(max_length=100)
    answer = models.TextField()
    position = models.TextField()
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)