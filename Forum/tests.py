from unittest.mock import MagicMock, patch
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Board, Thread, Post, PostImage
from .forms import NewThreadForm, PostForm
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from django.core.files import File

#
# @ Safari
#
# Resources Used: 
# https://docs.djangoproject.com/en/3.2/topics/testing/tools/
#


"""
UNIT TESTS
This app is more complex, so I am just trying to have some basic tests covering all the models, views, and forms
"""


'''
MODEL TESTS
'''
class BoardModelTest(TestCase):
    def test_board_creation(self):
        board = Board.objects.create(name="General Discussion", description="Talk about anything.")
        self.assertEqual(board.name, "General Discussion")
        self.assertEqual(board.description, "Talk about anything.")
        self.assertTrue(Board.objects.exists())

class ThreadModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john', email='john@example.com', password='123')
        self.board = Board.objects.create(name="General Discussion")

    def test_thread_creation(self):
        thread = Thread.objects.create(title="New Thread", board=self.board, starter=self.user)
        self.assertEqual(thread.title, "New Thread")
        self.assertEqual(thread.board, self.board)
        self.assertEqual(thread.starter, self.user)
        self.assertTrue(Thread.objects.filter(board=self.board).exists())

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john', email='john@example.com', password='123')
        self.board = Board.objects.create(name="General Discussion")
        self.thread = Thread.objects.create(title="New Thread", board=self.board, starter=self.user)

    def test_post_creation(self):
        post = Post.objects.create(message="Hello, world!", thread=self.thread, created_by=self.user)
        self.assertEqual(post.message, "Hello, world!")
        self.assertEqual(post.thread, self.thread)
        self.assertEqual(post.created_by, self.user)
        self.assertTrue(Post.objects.filter(thread=self.thread).exists())

class PostImageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john', email='john@example.com', password='123')
        self.board = Board.objects.create(name="General Discussion")
        self.thread = Thread.objects.create(title="New Thread", board=self.board, starter=self.user)
        self.post = Post.objects.create(thread=self.thread, message="Hello, world!", created_by=self.user)

    def test_post_image_creation(self):
        # Create an in-memory image file
        image = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        post_image = PostImage.objects.create(post=self.post, image=image)

        # Assert the image is saved correctly
        self.assertTrue(PostImage.objects.filter(id=post_image.id).exists())
        self.assertIn("test.jpg", post_image.image.name)  # Check if the file name is correct in the saved instance

    """
    NEEDS TO DELETE IMAGE AFTER TEST
    """
    def tearDown(self): 
        # Optionally, clean up after tests
        super().tearDown()

'''
FORM TESTS
'''
class NewThreadFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='john', password='12345')
        cls.board = Board.objects.create(name="General Discussion")

    def test_form_validity(self):
        form_data = {
            'title': 'Example Thread',
            'message': 'This is a test message for a new thread.'
        }
        form = NewThreadForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_save(self):
        form_data = {
            'title': 'Example Thread',
            'message': 'This is a test message for a new thread.'
        }
        files = {
            'image1': SimpleUploadedFile("file1.jpg", b"file_content1", content_type="image/jpeg"),
            'image2': SimpleUploadedFile("file2.jpg", b"file_content2", content_type="image/jpeg"),
            'image3': SimpleUploadedFile("file3.jpg", b"file_content3", content_type="image/jpeg")
        }
        form = NewThreadForm(data=form_data, files=files)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.starter = self.user  # Manually set the starter
            thread.board = self.board
            thread.save()
            form.save_m2m()  # Save images
            self.assertEqual(Thread.objects.count(), 1)
            self.assertEqual(thread.title, 'Example Thread')

#### PostForm Tests
class PostFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='john', password='12345')
        cls.board = Board.objects.create(name="General Discussion")
        cls.thread = Thread.objects.create(title="New Thread", board=cls.board, starter=cls.user)

    def test_post_form_validity(self):
        form_data = {
            'message': 'This is a new post message.'
        }
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_post_form_save(self):
        form_data = {
            'message': 'This is a new post message.'
        }
        file_data = {
            'image': SimpleUploadedFile("file.jpg", b"file_content", content_type="image/jpeg")
        }
        form = PostForm(data=form_data, files=file_data)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = self.user
            post.thread = self.thread
            post.save()
            form.save_m2m()  # Save the image
            self.assertEqual(Post.objects.count(), 1)
            self.assertEqual(post.message, 'This is a new post message.')

"""
VIEW TESTS
"""

class HomeViewTests(TestCase):
    def test_home_view_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')

    def test_home_view_context(self):
        Board.objects.create(name='Django', description='Django board.')
        response = self.client.get(reverse('home'))
        self.assertTrue('boards' in response.context)
        self.assertEqual(len(response.context['boards']), 1)

class BoardThreadsViewTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')

    def test_board_threads_view_status_code(self):
        response = self.client.get(reverse('board_threads', kwargs={'board_id': self.board.pk}))
        self.assertEqual(response.status_code, 200)

    def test_board_threads_view_not_found_status_code(self):
        response = self.client.get(reverse('board_threads', kwargs={'board_id': 9999}))
        self.assertEqual(response.status_code, 404)

    def test_board_threads_view_template(self):
        response = self.client.get(reverse('board_threads', kwargs={'board_id': self.board.pk}))
        self.assertTemplateUsed(response, 'board_threads.html')

class NewThreadViewTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        self.user = User.objects.create_user(username='john', password='123')
        self.client.login(username='john', password='123')

   #NEED TO BE FIXED

   #  def test_new_thread_view_status_code(self):
   #      response = self.client.get(reverse('new_thread', kwargs={'board_id': self.board.pk}))
   #      self.assertEqual(response.status_code, 200)

    def test_new_thread_view_redirect_after_post(self):
        data = {'title': 'Test thread', 'message': 'Hello'}
        response = self.client.post(reverse('new_thread', kwargs={'board_id': self.board.pk}), data)
        self.assertRedirects(response, reverse('board_threads', kwargs={'board_id': self.board.pk}))

class ReplyThreadViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john', password='123')
        self.board = Board.objects.create(name='Django', description='Django board.')
        self.thread = Thread.objects.create(title="New Thread", board=self.board, starter=self.user)
        self.client.login(username='john', password='123')

   #NEED TO BE FIXED

   #  def test_reply_thread_view_status_code(self):
   #      response = self.client.get(reverse('reply_thread', kwargs={'thread_id': self.thread.pk}))
   #      self.assertEqual(response.status_code, 200)

    def test_reply_thread_view_redirect_after_post(self):
        data = {'message': 'A reply to the thread.'}
        response = self.client.post(reverse('reply_thread', kwargs={'thread_id': self.thread.pk}), data)
        self.assertRedirects(response, reverse('thread_posts', kwargs={'thread_id': self.thread.pk}))