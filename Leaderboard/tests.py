from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from Leaderboard.views import leaderboard_view
from UserAuth.models import UserProfile
from django.contrib.auth.decorators import login_required

class LeaderboardViewTests(TestCase):
    def setUp(self):
        """
        Set up the necessary objects and data for the test case.

        This method is called before each test method is executed.

        - Creates a RequestFactory object.
        - Creates a test user with the username 'testuser' and password '12345'.
        - Retrieves or creates a UserProfile object for the test user.

        """

        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.profile = UserProfile.objects.get_or_create(user=self.user)[0]

    def test_access_denied_to_anonymous_users(self):
        """
        Test that anonymous users are denied access to the leaderboard view.
        """

        request = self.factory.get('/leaderboard')
        request.user = AnonymousUser()
        response = leaderboard_view(request)
        self.assertEqual(response.status_code, 302)  # Assuming redirect to login

    def test_access_granted_to_authenticated_users(self):
        """
        Test that access is granted to authenticated users.

        This test checks if the view '/leaderboard' returns a status code of 200
        when accessed by an authenticated user.

        """
        
        request = self.factory.get('/leaderboard')
        request.user = self.user
        response = leaderboard_view(request)
        self.assertEqual(response.status_code, 200)
