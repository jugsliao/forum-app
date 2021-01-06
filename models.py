from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Question(models.Model):
    '''A question a student is writing about'''
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="question", null=True) # <--- added
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''return a string represetation of the model'''
        return self.text

class Answer(models.Model):
    '''Answers to a specific question'''
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
