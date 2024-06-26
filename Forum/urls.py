from django.urls import path
from .views import home, board_threads, thread_posts, new_thread, reply_thread, user_profile, delete_thread, delete_post, edit_post, edit_thread

urlpatterns = [
    path('', home, name='home'),
    path('board/<int:board_id>/', board_threads, name='board_threads'),
    path('thread/<int:thread_id>/', thread_posts, name='thread_posts'),
    path('board/<int:board_id>/new/', new_thread, name='new_thread'),
    path('thread/<int:thread_id>/reply/', reply_thread, name='reply_thread'),
    path('user/<str:username>/', user_profile, name='user_profile'),
    path('thread/<int:thread_id>/delete/', delete_thread, name='delete_thread'),
    path('thread/<int:thread_id>/post/<int:post_id>/delete/', delete_post, name='delete_post'),
    path('thread/<int:thread_id>/edit/', edit_thread, name='edit_thread'),
    path('post/<int:post_id>/edit/', edit_post, name='edit_post'),
]
