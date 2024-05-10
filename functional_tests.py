import unittest
from selenium import webdriver

class NewVisitorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
    
    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_start_a_todo_list(self):
        # User goes to check out the home page
        self.browser.get("http://localhost:8000")

        # She notices the page title and header mention to-do lists
        self.assertIn("To-Do", self.browser.title)

        # She is invited to enter a to-do item straight away
        self.fail("Finish the test!")

        # She types "Buy peacock feathers" into a text box

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list

        # There is still a text box inviting her too add another item.
        # She enters "Use peacock feathers to make a fly"

        # The page updates again, and now shows both items on her lists

        # Satisfied, she goes back to sleep

if __name__ == "__main__":
    unittest.main()