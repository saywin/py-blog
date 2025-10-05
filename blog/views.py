from django.core.paginator import Paginator
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseRedirect,
)
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from blog.models import Post, Commentary


def index(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.order_by("-created_time")
    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"post_list": page_obj, "page_obj": page_obj}
    return render(request, "blog/index.html", context=context)


class PostDetailView(generic.DetailView):
    model = Post
    template_name = "blog/post_detail.html"

    def post(self, request, *args, **kwargs) -> HttpResponse:
        comment = request.POST["add_comment"]

        if comment and request.user.is_authenticated:
            post = self.get_object()
            Commentary.objects.create(
                content=comment, user=request.user, post=post
            )
            return HttpResponseRedirect(
                reverse("blog:post-detail", kwargs={"pk": post.pk})
            )
        return HttpResponseBadRequest("Comment cannot be empty")
