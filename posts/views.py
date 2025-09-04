# posts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions

from .models import Post, Comment
from .forms import PostForm, CommentForm
from .serializers import PostSerializer, CommentSerializer

User = get_user_model()


# ----------------- HTML VIEWS -----------------

@login_required
def create_post(request):
    """
    Create a new post (text or image)
    """
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("core:feed")
    else:
        form = PostForm()
    return render(request, "posts/create_post.html", {"form": form})


@login_required
def add_comment(request, post_id):
    """
    Add a comment to a post
    """
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
    return redirect("core:feed")


@login_required
def profile_view(request, user_id):
    """
    Display a user's profile and their posts
    """
    profile_user = get_object_or_404(User, id=user_id)
    user_posts = Post.objects.filter(author=profile_user).order_by('-created_at')

    # Followers/following (optional if you have Follow model)
    followers_count = profile_user.followers.count() if hasattr(profile_user, 'followers') else 0
    following_count = profile_user.following.count() if hasattr(profile_user, 'following') else 0
    is_following = profile_user.followers.filter(follower=request.user).exists() if hasattr(profile_user,
                                                                                            'followers') else False

    return render(request, 'posts/profile.html', {
        'profile_user': profile_user,
        'user_posts': user_posts,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following
    })

@login_required
def user_search(request):
    """
    Search users by username
    """
    query = request.GET.get('q')
    results = User.objects.filter(username__icontains=query) if query else []
    return render(request, 'accounts/user_search_results.html', {'results': results, 'query': query})


# ----------------- API VIEWS -----------------

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def posts_api(request):
    """
    GET: List all posts
    POST: Create a new post
    """
    if request.method == 'GET':
        posts = Post.objects.all().order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def comment_api(request, post_id):
    """
    POST: Add comment to a post
    """
    post = get_object_or_404(Post, id=post_id)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(post=post, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
