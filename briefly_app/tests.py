from django.test import TestCase
from django.urls import reverse
from briefly_app.models import BrieflyUser, Category, UserCategory, NewsArticle


# Create your tests here.

class UserViewsTestCases(TestCase):
    def setUp(self):
        self.user = BrieflyUser.objects.create_user(username="testuser", email="test@email.com", password="testpassword")
        self.category = Category.objects.create(CategoryName="Technology")

        self.client.login(username='testuser', password='testpassword')
        
        UserCategory.objects.create(User=self.user, Category=self.category)

        NewsArticle.objects.create(
            Title="Tech News",
            Content="Latest in tech.",
            Source="TechSource",
            Category=self.category
        )

    # def test_user_signup(self):

    #     BrieflyUser.objects.all().delete()

    #     url = reverse("briefly:user_signup")
    #     form_data = {
    #         'username': 'testuser',
    #         'password': 'testpassword',
    #         'password_confirmation': 'testpassword',
    #         'country': 'in',
    #         # 'categories': [''],
    #     }
    #     response = self.client.post(reverse('briefly:user_signup'), form_data)
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, reverse('briefly:user_login'))

    # def test_user_signup(self):
    #     response = self.client.get(reverse('briefly:user_signup'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'signup.html')

    def test_user_login(self):
        url = reverse('briefly:user_login')
        form_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }

        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 302)  # 302 - redirect after successful login
        self.assertRedirects(response, reverse('briefly:top_page'))

        print("\n---\nSUCCESS: test_user_login \n---")

    def test_user_logout(self):
        self.client.login(username="testuser", password="testpassword")
        url = reverse('briefly:user_logout')
        response = self.client.post(url)
        self.assertRedirects(response, reverse('briefly:top_page'))

        print("\n---\nSUCCESS: test_user_logout \n---")


    def test_get_user_news(self):
        url = reverse('briefly:user_news', kwargs={'username': self.user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('news', response_data)

        print("\n---\nSUCCESS: test_get_user_news \n---")

    def test_get_user_news_other_user(self):
        other_user = BrieflyUser.objects.create_user(username="otheruser", email="other@email.com", password="otherpassword")
        self.client.login(username='otheruser', password='otherpassword')
        print("\n|- other user logged in, trying to access self user url \n")


        url = reverse('briefly:user_news', kwargs={'username': self.user.username}) # other user trying to access self user url
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403) # 403 - forbidden
        response_data = response.json()
        self.assertIn('error', response_data)

        print("\n---\nSUCCESS: test_get_user_news_other_user \n---")
