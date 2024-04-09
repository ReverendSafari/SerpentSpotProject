from django.shortcuts import render, redirect, get_object_or_404
from .models import Board, Thread, Post, User
from .forms import NewThreadForm, PostForm
from django.contrib.auth.decorators import login_required

def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})

def board_threads(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    return render(request, 'board_threads.html', {'board': board, 'threads': board.threads.all()})

def thread_posts(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    return render(request, 'thread_posts.html', {'thread': thread, 'posts': thread.posts.all()})

@login_required
def new_thread(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    if request.method == 'POST':
        form = NewThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.board = board
            thread.starter = request.user
            thread.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                thread=thread,
                created_by=request.user
            )
            return redirect('thread_posts', thread_id=thread.id)  # Redirect to the new thread's page
    else:
        form = NewThreadForm()
    return render(request, 'new_thread.html', {'board': board, 'form': form})

@login_required
def reply_thread(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.thread = thread
            post.created_by = request.user
            post.save()
            return redirect('thread_posts', thread_id=thread.id)
    else:
        form = PostForm()
    return render(request, 'reply_thread.html', {'thread': thread, 'form': form})

def user_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'user_profile.html', {'user': user})
