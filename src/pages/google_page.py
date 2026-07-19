from pages.base_page import BasePage
from locators.google_locators import GoogleLocators
from utils.logger import get_logger


logger = get_logger(__name__)


class GooglePage(BasePage):

    def open(self, base_url):
        logger.info("Opening application URL: %s", base_url)
        super().open(base_url)

    def search(self, text):
        logger.info("Searching for: %s", text)
        self.enter_text(
            GoogleLocators.SEARCH_BOX,
            text,
        )