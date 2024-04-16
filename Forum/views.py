from django.shortcuts import render, redirect, get_object_or_404
from .models import Board, Thread, Post, User
from .forms import NewThreadForm, PostForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages


def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})

def board_threads(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    form = NewThreadForm()  # Instantiate the form
    return render(request, 'board_threads.html', {'board': board, 'threads': board.threads.all(), 'form': form})

def thread_posts(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    form = PostForm()  # Instantiate the form
    return render(request, 'thread_posts.html', {'thread': thread, 'posts': thread.posts.all(), 'form': form})

@login_required
def new_thread(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    if request.method == 'POST':
        form = NewThreadForm(request.POST, request.FILES, instance=Thread(starter=request.user, board=board))
        if form.is_valid():
            thread = form.save()
            messages.success(request, 'New thread created successfully!')
            return redirect('board_threads', board_id=board.id)
        else:
            messages.error(request, 'Error creating thread. Please check the form data.')
    else:
        form = NewThreadForm(instance=Thread(starter=request.user, board=board))
    return render(request, 'new_thread.html', {'form': form})


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

            messages.success(request, 'Your reply has been posted!')
            return redirect('thread_posts', thread_id=thread.id)  # Redirect to the thread view or wherever appropriate
        else:
            messages.error(request, 'There was an error with your post. Please check your input.')
    else:
        form = PostForm()

    return render(request, 'reply_thread.html', {'form': form, 'thread': thread})

def user_profile(request, username):
    # Optional: You might still want to check if the user exists to handle errors
    user = get_object_or_404(User, username=username)
    # Redirect to the desired URL in the other app
    return redirect(f'/auth/profile/{username}/')

@login_required
def delete_thread(request, thread_id):
    if request.method == 'POST':
        thread = get_object_or_404(Thread, pk=thread_id, starter=request.user)
        thread.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False}, status=400)