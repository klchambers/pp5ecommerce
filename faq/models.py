from django.db import models
from django.contrib.auth.models import User

STATUS = ((0, "Draft"), (1, "Published"))


# Create your models here.
class Faq(models.Model):
    question = models.CharField(max_length=254)
    answer = models.TextField(blank=True)
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    status = models.IntegerField(choices=STATUS, default=0)

    def __str__(self):
        return f"'{self.question}' asked by {self.user}"
