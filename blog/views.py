from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from blog.models import Tag, Post


def post_list(request,category_id=None,tag_id=None):
    if tag_id: #标签
        try:
            tag=Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            post_list=[]
        else:
            post_list=tag.post_set.filter(status=Post.STATUS_NORMAL)
    elif category_id: #分类
        post_list = Post.objects.filter(status=Post.STATUS_NORMAL,category_id=category_id)
    else: #主页
        post_list=Post.objects.filter(status=Post.STATUS_NORMAL)

    return render(request,'blog/list.html',context={'post_list':post_list})

def post_detail(request,post_id):
    try:
        post=Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post=None
    return render(request,'blog/detail.html',context={'post':post})