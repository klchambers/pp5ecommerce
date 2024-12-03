from django.shortcuts import render, get_object_or_404
from .models import BlogPost


# Create your views here.
def blog(request):
    posts = BlogPost.objects.filter(status=1).order_by('-posted_on')
    return render(request, 'blog/blog.html', {'posts': posts})


def blog_post(request, id):
    post = get_object_or_404(BlogPost, id=id)
    return render(request, 'blog/blog_post.html', {'post': post})
