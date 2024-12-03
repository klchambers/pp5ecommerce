from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

STATUS = ((0, "Draft"), (1, "Published"))


# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=254, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    featured_image = CloudinaryField('image', blank=True)
    post = models.TextField()
    posted_on = models.DateField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    def __str__(self):
        return f"{self.title} | posted by {self.author} on {self.posted_on}"
