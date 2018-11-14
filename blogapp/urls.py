from django.urls import path
from blogapp.views import read_blog, edit_post,write_post, get_unpublished_posts




urlpatterns = [
    path('unpublished', get_unpublished_posts, name='get_unpublished_posts'),
    path('read_blog/<int:id>', read_blog, name="read_blog"),
    path('edit_post/<int:id>', edit_post, name="edit_post"),
    path('write_post/', write_post, name="write_post"),
   
    
    ]