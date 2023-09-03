import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://www.nhl.com/news/"


class NHL:
    def __init__(self, teardown=True):

        s = Service(ChromeDriverManager().install())
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        # self.teardown = teardown
        # keep chrome open
        self.options.add_experimental_option("detach", True)
        self.options.add_experimental_option(
            "excludeSwitches",
            ['enable-logging'])
        self.driver = webdriver.Chrome(
            options=self.options,
            service=s)
        self.driver.implicitly_wait(50)
        self.detail_links = []
        self.collection = []
        super(NHL, self).__init__()

    def __enter__(self):
        self.driver.get(BASE_URL)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.driver.quit()

    def land_first_page(self):
        self.driver.get(BASE_URL)

    def get_archive(self):
        """
        this is used to get the archive per month base on the number
        :return:
        """

        self.driver.get(f"{BASE_URL}")
        # load all content of the page
        self.load_all_content_on_page()
        # after getting the links
        # get each detail
        print("Getting Details")
        self.get_all_detail_page()
        self.get_details()

    def load_all_content_on_page(self):
        # Get the initial height of the page
        initial_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll to the bottom of the page
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait for a short time for content to load (adjust as needed)
            time.sleep(2)

            # Get the updated height of the page
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            # If the page height hasn't changed, it means all content has been loaded
            if new_height == initial_height:
                break

            initial_height = new_height
        return

    def get_all_detail_page(self):
        """
        this is used to get the detail links of all page
        :return:
        """
        detail_elements = self.driver.find_elements(
            by=By.CSS_SELECTOR, value='a[class="article-item__more"]'
        )
        for detail_element in detail_elements:
            self.detail_links.append(f'{detail_element.get_attribute("href")}')
        print(len(self.detail_links))
        with open("detail_links.json", "w") as file:
            file.write(json.dumps(self.detail_links))

    def get_details(self):
        """
        this is used to get the detail links of all page
        :return:
        """
        blog_content = {}
        for item in self.detail_links:
            self.driver.get(item)
            slug = item.split("/")[-1].replace(".html", "")

            try:

                blog_content["slug"] = slug
                blog_content["category"] = "NHL"
                blog_content["title"] = self.driver.find_element(
                    by=By.CSS_SELECTOR,
                    value='h1[class="article-item__headline"]').get_attribute(
                    "innerHTML")
                try:
                    blog_content["image_url"] = self.driver.find_element(
                        by=By.CSS_SELECTOR,
                        value='img[class="article-item__img "]').get_attribute("src")
                except:
                    pass
                blog_content["detail"] = self.driver.find_element(
                    by=By.CSS_SELECTOR,
                    value='div[class="article-item__body"]'
                ).get_attribute("innerHTML")
                self.collection.append(blog_content)
                with open("collection.json", "w") as file:
                    file.write(json.dumps(self.collection))

            except Exception as a:
                print(a)
                pass
