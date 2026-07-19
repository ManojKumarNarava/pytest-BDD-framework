from playwright.sync_api import Page


class BasePage:

    def __init__(self, page: Page):
        self.page = page

    def open(self, url):
        self.page.goto(url)

    def click(self, locator):
        self.page.locator(locator).click()

    def enter_text(self, locator, text):
        self.page.locator(locator).fill(text)

    def get_text(self, locator):
        return self.page.locator(locator).text_content()

    def get_title(self):
        return self.page.title()

    def wait(self, locator):
        self.page.locator(locator).wait_for()

    def screenshot(self, name):
        self.page.screenshot(path=f"screenshots/{name}.png")