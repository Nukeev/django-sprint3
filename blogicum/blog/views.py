from django.shortcuts import get_object_or_404, render

from django.utils import timezone

from .models import Post, Category

def index(request):
    current_time = timezone.now()
    posts = Post.objects.filter(
        pub_date__lte=current_time,
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')[:5]
    return render(request, 'blog/index.html', {'posts': posts})

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
    category = get_object_or_404(Category, slug=category_slug, is_published=True)

    posts = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=current_time
    ).order_by('-pub_date')

    return render(
        request,
        'blog/category.html',
        {'category': category, 'posts': posts}
    )
