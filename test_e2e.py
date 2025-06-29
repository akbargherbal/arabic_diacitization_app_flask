# test_e2e.py

from playwright.sync_api import Page, expect

# All our tests will be functions that start with `test_`
# The `page` argument is a magic fixture provided by pytest-playwright.
# It represents a browser tab.


def test_initial_page_load_and_focus(page: Page):
    """
    Tests that the page loads correctly and the first interactive
    character is automatically focused.
    """
    # ARRANGE & ACT: Go to the application's homepage.
    # Make sure your Flask app is running before you run this test.
    page.goto("http://127.0.0.1:5000/")

    # ASSERT: Now we check if the page is in the state we expect.

    # 1. Check if the page title is correct.
    expect(page).to_have_title("Diacritic Editor - Final Mockup")

    # 2. Find the first diacritic span using its unique data attribute.
    #    This is the span that should have the focus class.
    #    A locator is Playwright's way of finding an element.
    first_char_focus_span = page.locator("[data-global-dia-idx='0'][data-dia]")

    # 3. Assert that this specific element has the 'char-focus' class.
    #    This is the automated equivalent of us visually checking for the blue underline.
    expect(first_char_focus_span).to_have_class("char char-focus")

    # 4. As a bonus, let's check that the *second* character does NOT have focus.
    second_char_focus_span = page.locator("[data-global-dia-idx='1'][data-dia]")
    expect(second_char_focus_span).not_to_have_class("char-focus")


def test_mouse_click_navigation(page: Page):
    """
    Tests if clicking a character correctly moves the focus.
    """
    # ARRANGE
    page.goto("http://127.0.0.1:5000/")

    # CORRECTED LOCATORS: Target the VISIBLE base character span.
    first_char_base_span = page.locator("[data-global-char-idx='0']")
    fifth_char_base_span = page.locator("[data-global-char-idx='5']")

    # We still check the focus on the diacritic span, because that's where the class is.
    first_char_focus_span = page.locator("[data-global-dia-idx='0'][data-dia]")
    fifth_char_focus_span = page.locator("[data-global-dia-idx='5'][data-dia]")

    # Initial assertion: Make sure focus is on the first character.
    expect(first_char_focus_span).to_have_class("char char-focus")
    expect(fifth_char_focus_span).not_to_have_class("char-focus")

    # ACT
    # CORRECTED ACTION: Click the VISIBLE base character span.
    fifth_char_base_span.click()

    # ASSERT
    # The assertion remains the same.
    expect(first_char_focus_span).not_to_have_class("char-focus")
    expect(fifth_char_focus_span).to_have_class("char-focus")
