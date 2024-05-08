from django.shortcuts import render, redirect, get_object_or_404
from .models import Board, PostImage, Thread, Post, User
from .forms import NewThreadForm, PostForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed, JsonResponse
from django.contrib import messages

#
# @ Safari
# 
# Resources used:
# 
# https://reintech.io/blog/django-forum-tutorial-build-a-forum-in-django-step-by-step-guide-for-software-developers
# https://chat.openai.com/share/3b5f37f4-0ab6-4670-acda-060bfa5d6331
# https://chat.openai.com/share/b307d523-910e-45e0-b978-cd4f0e77e0f5
# 

"""
Renders the home page template, displaying all boards and latest 5 threads

Args:
    request: The request object.

Returns:
    render object: The render object for the home page template. (Include all boards and latest threads)
"""

def home(request):
    boards = Board.objects.all() # Fetch all boards
    threads = Thread.objects.order_by('-created_at')[:5] # Fetch the latest 5 threads
    posts = Post.objects.order_by('-created_at')[:5]  # Fetch the latest 5 posts
    return render(request, 'home.html', {'boards': boards, 'threads': threads, 'posts': posts}) 

"""
Renders the board of the given ID, displaying all threads in the board

Args:
    request: The request object.
    board_id: The ID of the board to display.

Returns:
    render object: The render object for the board template. (all threads on that board and the board title)
"""
def board_threads(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    form = NewThreadForm()  # Instantiate the form
    threads = board.threads.all().order_by('-created_at')
    return render(request, 'board_threads.html', {'board': board, 'threads': threads, 'form': form})

"""
Renders the thread of the given ID, displaying all replies in the thread

Args:
    request: The request object.
    thread_id: The ID of the thread to display.

Returns:
    render object: The render object for the thread template. (all posts on that thread and the thread title)
"""

def thread_posts(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    form = PostForm()  # Instantiate the form
    return render(request, 'thread_posts.html', {'thread': thread, 'posts': thread.posts.all(), 'form': form})

"""
Creates a new thread in the given board

Args:
    request: The request object.
    board_id: The ID of the board to create the thread in.

Returns:
    redirect object: Redirects to the board threads page after creating the thread.
"""
@login_required
def new_thread(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    if request.method == 'POST':
        form = NewThreadForm(request.POST, request.FILES, instance=Thread(starter=request.user, board=board))
        if form.is_valid():
            thread = form.save()
            return redirect('board_threads', board_id=board.id)
        else:
            messages.error(request, 'Error creating thread. Please check the form data.')
    else:
        return HttpResponseNotAllowed(['POST'], "Invalid request method. Please use POST.")

"""
Creates a new reply on a given thread

Args:
    request: The request object.
    thread_id: The ID of the thread to reply to.

Returns:
    redirect object: Redirects to the thread posts page after creating the post.
"""

@login_required
def reply_thread(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # Ensure to include request.FILES to handle image uploads
        if form.is_valid():
            post = form.save(commit=False)
            post.thread = thread  # Set the thread for the post
            post.created_by = request.user  # Set the user who created the post
            post.save()
            form.save()  # Save the form to handle image saving as per the form's save method

            return redirect('thread_posts', thread_id=thread.id)  # Redirect to the thread view or wherever appropriate
        else:
            messages.error(request, 'There was an error with your post. Please check your input.')
    else:
        return HttpResponseNotAllowed(['POST'], "Invalid request method. Please use POST.")

"""
Redriects to the user profile page

Args:
    request: The request object.
    username: The username of the user to view the profile of.

Returns:
    redirect object: Redirects to the user profile page.
"""
def user_profile(request, username):
    # We might still want to check if the user exists to handle errors
    user = get_object_or_404(User, username=username)
    # Redirect to the desired URL in the other app
    return redirect(f'/auth/profile/{username}/')

"""
Deletes a thread with the given ID

Args:
    request: The request object.
    thread_id: The ID of the thread to delete.

Returns:
    JsonResponse object: Returns a JSON response indicating success or failure.
"""
@login_required
def delete_thread(request, thread_id):
    if request.method == 'POST':
        thread = get_object_or_404(Thread, pk=thread_id, starter=request.user)
        thread.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False}, status=400)

"""
Deletes a reply with the given ID's of the thread and reply

Args:
    request: The request object.
    thread_id: The ID of the thread the reply belongs to.
    post_id: The ID of the reply to delete.

Returns:
    JsonResponse object: Returns a JSON response indicating success or failure.
"""
@login_required
def delete_post(request, thread_id, post_id):
    post = get_object_or_404(Post, pk=post_id, created_by=request.user, thread_id=thread_id)  # Validates post belongs to thread
    if request.method == 'POST':
        post.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False}, status=400)

"""
Allows the user to edit a reply with the given ID of the post

Args:
    request: The request object.
    post_id: The ID of the post to edit.

Returns:
    redirect object: Redirects to the thread (refreshes) after editing the post.
"""
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, created_by=request.user)  # Ensure only the creator can edit
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            images_to_delete = request.POST.getlist('images_to_delete[]')  # Fetch the list of image ids marked for deletion
            for image_id in images_to_delete:
                image = PostImage.objects.get(id=image_id)
                image.delete()  # Delete the selected images

            form.save()
            return redirect('thread_posts', thread_id=post.thread.id)
        else:
            messages.error(request, 'Error updating the post.')
    else:
        return HttpResponseNotAllowed(['POST'], "Invalid request method. Please use POST.")

"""
Allows the user to edit a thread

Args:
    request: The request object.
    thread_id: The ID of the thread to edit.

Returns:
    render object: The render object for the edit thread page.
"""

@login_required
def edit_thread(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id, starter=request.user)
    initial_post = thread.posts.first()  # Assuming the first post is the main thread post
    if request.method == 'POST':
        thread.title = request.POST.get('title')
        initial_post.message = request.POST.get('message')
        images_to_delete = request.POST.getlist('images_to_delete[]')
        for image_id in images_to_delete:
            image = PostImage.objects.get(id=image_id, post=initial_post)
            image.delete()
        thread.save()
        initial_post.save()
        messages.success(request, 'Thread updated successfully!')
        return redirect('thread_posts', thread_id=thread.id)
    return HttpResponseNotAllowed(['POST'], "Invalid request method. Please use POST.")
