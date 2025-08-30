from playwright.sync_api import sync_playwright


class Webdriver:
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.browser = None

    def initialize_context_page(self):
        p = sync_playwright().start()

        self.browser = p.chromium.launch(headless=self.headless)

        self.context = self.browser.new_context()

        return self.context.new_page()

    def quit(self):
        if self.browser:
            self.browser.close()
