from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from django.views import View
from .forms import CommentForm

from datetime import date
from .models import Author, Tag, Post

# Create your views here.

## Craeting Class Based View
class IndexPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts" # define the key name for access posts

    def get_queryset(self): # this function defines how query will execute
        queryset = super().get_queryset()
        data = queryset[:3]
        return data


# def index(request):
#     latest_posts = Post.objects.all().order_by("date")[:3]
#     return render(request, "blog/index.html", {
#         "posts": latest_posts
#     })   

class AllPostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

class PostDetailsPageView(View):
    def get(self, request, slug):
        post = Post.objects.get(slug = slug)
        read_later_active = False

        if request.session.get("stored_posts"):
            if post.id in request.session.get("stored_posts"):
                read_later_active = True

        return render(request, "blog/post-detail.html", {
            "post" : post,
            "post_tags" : post.tags.all(),
            "read_later_active" : read_later_active,
            "form" : CommentForm(),
            "all_comments" : post.comments.all().order_by("-id")
            })

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug = slug)
        
        if comment_form.is_valid():
            comment_obj = comment_form.save(commit=False) # comment_obj is instance of comment model
            comment_obj.post = post
            comment_obj.save()
            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))

        if request.session.get("stored_posts"):
            if post.id in request.session.get("stored_posts"):
                read_later_active = True

        return render(request, "blog/post-detail.html", {
            "post" : post,
            "post_tags" : post.tags.all(),
            "read_later_active" : read_later_active,
            "form" : comment_form,
            "all_comments" : post.comments.all().order_by("-id")
            })

class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")

        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context["has_posts"] = False

        else:
            saved_posts = Post.objects.filter(id__in = stored_posts)

            for post in saved_posts:
                post.content = post.content[:71]

            context["has_posts"] = True
            context["posts_list"] = saved_posts

        return render(request, 'blog/read-later.html', context)

    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None or len(stored_posts) == 0:
            stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)

        request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect("/")
