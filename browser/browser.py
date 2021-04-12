from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path


class WebBrowser:
    browser: object = None

    def __init__(self):
        # The following options are required to make headless Chrome
        # work in a Docker container
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("window-size=1024,768")
        self.chrome_options.add_argument("--no-sandbox")

    def init_app(self):
        self.browser = webdriver.Chrome(chrome_options=self.chrome_options)
        return self.browser


browser_instance = WebBrowser().init_app()