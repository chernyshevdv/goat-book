from django.test import TestCase
from django.http import HttpRequest
from lists.views import home_page
from lists.models import Item, List

class HomePageTest(TestCase):
    def test_homepage_returns_correct_html(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_dont_save_empty_items(self):
        response = self.client.get("/")
        self.assertEqual(0, Item.objects.count())


class NewListTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        todo_text = "A new list item"
        response = self.client.post(f"/lists/{correct_list.id}/add_item", data={"item_text": todo_text})
        self.assertEqual(Item.objects.count(), 1)
        saved_item = Item.objects.get()
        self.assertEqual(saved_item.text, todo_text)
        self.assertEqual(saved_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.post(f"/lists/{correct_list.id}/add_item", data={"item_text": "A new item"})
        self.assertRedirects(response, f"/lists/{correct_list.id}/")
    

class ListViewTest(TestCase):
    def test_uses_list_template(self):
        my_list = List.objects.create()
        response = self.client.get(f"/lists/{my_list.id}/")
        self.assertTemplateUsed(response, "list.html")


    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        todo_items = ["A todo number one", "A todo number to"]
        for item in todo_items:
            Item.objects.create(text=item, list=correct_list)
        
        other_list = List.objects.create()
        Item.objects.create(text="Another list item", list=other_list)
        response = self.client.get(f"/lists/{correct_list.id}/")
        for item in todo_items:
            self.assertContains(response, item)
        self.assertNotContains(response, "Another list item")

class ListAndItemModelsTest(TestCase):
    def test_saving_and_retrieving_items(self):
        my_list = List()
        my_list.save()

        first_item = Item()
        first_item.list = my_list
        first_item.text = "The first (ever) list item"
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.list = my_list
        second_item.save()

        saved_list = List.objects.get() # there is just one
        self.assertEqual(saved_list, my_list)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(first_saved_item.list, my_list)
        self.assertEqual(second_saved_item.text, "Item the second")
        self.assertEqual(second_saved_item.list, my_list)
