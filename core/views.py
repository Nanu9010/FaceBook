from posts.forms import CommentForm
from posts.models import Post
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def feed(request):
    """
    Display homepage feed with all posts
    """
    posts = Post.objects.all().order_by("-created_at")
    comment_form = CommentForm()
    return render(request, "core/feed.html", {"posts": posts, "comment_form": comment_form})

