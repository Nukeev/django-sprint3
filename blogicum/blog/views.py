from django.shortcuts import get_object_or_404, render

from django.utils import timezone

from .models import Post, Category


POSTS_ON_INDEX_LIMIT = 5

def index(request):
    post_list = Post.objects.published()[:POSTS_ON_INDEX_LIMIT]
    return render(request, 'blog/index.html', {'post_list': post_list})

def post_detail(request, post_id):
    current_time = timezone.now()
    post = get_object_or_404(
        Post.objects.select_related('category'),
        pk=post_id,
        is_published=True,
        pub_date__lte=current_time,
        category__is_published=True
    )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    current_time = timezone.now()
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )

    post_list = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=current_time
    ).order_by('-pub_date')

    return render(
        request,
        'blog/category.html',
        {'category': category, 'post_list': post_list}
    )
