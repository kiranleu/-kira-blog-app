from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from .models import Post
from .forms import PostForm

# Create your views here.

def is_in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


def user_can_edit_post(request, post):
    wrote_the_post = post.author == request.user
    is_editor = is_in_group(request.user, 'editors')
    superuser = request.user.is_superuser
    return wrote_the_post or superuser or is_editor
    
# def author_can_add_new_post(request, post):
#     add_new_post = post.author == request.user
#     is_author = is_in_group(request.user, 'authors')
#     superuser = request.user.is_superuser
#     return add_new_post or superuser or is_author
    
def show_all(request):
    posts = Post.objects.filter(published_date__lte = timezone.now())
    
    return render(request, "blogapp/get_index.html", {'posts': posts})

def read_blog(request,id):
    blog = Post.objects.get(pk=id)
    blog.views +=1
    blog.save()
    can_edit = user_can_edit_post(request, blog)
    can_publish = is_in_group(request.user, 'publishers')
    
    
    # is_editor = request.user.groups.filter(name='editors').extists()
    print(request.user.groups.all())
    
    return render(request,"blogapp/read_post.html",{'blog': blog, 'can_edit':can_edit, 'can_publish': can_publish})
    
   
def edit_post(request,id):
   blog=Post.objects.get(pk=id)
   if request.method=="POST":
        form = PostForm(request.POST, request.FILES,instance=blog)
        form.save()
        return redirect("/read_blog/{0}".format(id))
   else:
       form=PostForm(instance=blog)
       return render(request,"blogapp/post_form.html",{'form':form})
       
@login_required
def write_post(request):
    if request.method=="POST":
        form = PostForm(request.POST, request.FILES)
        blog = form.save(commit=False)
        blog.author = request.user
        blog.save()
        return redirect(read_blog, blog.id)
    else:
        form = PostForm()
        return render(request, "blogapp/post_form.html", {'form':form})
        
def get_unpublished_posts(required,id):
   posts=Post.objects.filter(published_date__gtel=timezone.now())
   return render(request,"blog/get_index.html",{'posts':posts})

@permission_required('blog.can_publish', 'blog_change_post')
def publish_post(request, id):
    post = get_object_or_404(Post , pk=id)
    post.published_date = timezone.now()
    post.save()
    return redirect(read_post, post.id)