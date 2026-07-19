from playwright.sync_api import Playwright, Browser


class BrowserManager:

    @staticmethod
    def launch_browser(
        playwright: Playwright,
        browser_name: str,
        headless: bool,
    ) -> Browser:

        browser_name = browser_name.lower()

        if browser_name == "firefox":
            return playwright.firefox.launch(headless=headless)

        if browser_name == "webkit":
            return playwright.webkit.launch(headless=headless)

        if browser_name == "chromium":
            return playwright.chromium.launch(headless=headless)

        raise ValueError(
            f"Unsupported browser: {browser_name}. "
            "Use chromium, firefox or webkit."
        )