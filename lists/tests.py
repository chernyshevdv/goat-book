from django.test import TestCase
from django.http import HttpRequest
from lists.views import home_page

class HomePageTest(TestCase):
    def test_homepage_returns_correct_html(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")
    
    def test_can_save_a_POST_request(self):
        todo_text = "A new list item"
        response = self.client.post("/", data={"item_text": todo_text})
        self.assertContains(response, todo_text)
