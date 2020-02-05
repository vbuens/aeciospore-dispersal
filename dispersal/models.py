from django.db import models
from django.utils import timezone
# Create your models here

class Question(models.Model):
    question_text = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=50)

    def __str__(self):
        return self.answer_text


class EntryRequest(models.Model):
    country = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    wind = models.CharField(max_length=200)
    bushperc = models.DecimalField(max_digits=5,decimal_places=2)
    leafperc = models.DecimalField(max_digits=5,decimal_places=2)
    Q = models.CharField(max_length=200)
    height = models.CharField(max_length=200)
    stability_class = models.CharField(max_length=200)

    requested_date = models.DateTimeField(default=timezone.now())
