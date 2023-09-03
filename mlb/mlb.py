import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://www.sbnation.com/archives/mlb/2023/"


class MLB:
    def __init__(self, teardown=True):

        s = Service(ChromeDriverManager().install())
        self.options = webdriver.ChromeOptions()
        # self.options.add_argument('headless')
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
        super(MLB, self).__init__()

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

        for item in range(1, 9):
            self.driver.get(f"{BASE_URL}{item}")
            # load all content of the page
            self.load_all_content_on_page()
        # after getting the links
        # get each detail
        print("Getting Details")
        self.get_details()

    def load_all_content_on_page(self):
        while True:
            try:
                button_to_click = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, 'button[class="p-button c-archives-load-more__button"]'))
                )
                button_to_click.click()
                time.sleep(3)
                print("Clicked the 'Load More' button.")
            except Exception as a:
                print("'Load More' button not found. No action taken.")
                # if there is no more load more  button the get all detail link
                self.get_all_detail_page()
                return

    def get_all_detail_page(self):
        """
        this is used to get the detail links of all page
        :return:
        """
        detail_elements = self.driver.find_elements(
            by=By.CSS_SELECTOR, value='a[data-chorus-optimize-field="hed"]'
        )
        for detail_element in detail_elements:
            self.detail_links.append(detail_element.get_attribute("href"))
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
            print(item)
            self.driver.get(item)
            slug = item.split("/")[-1]
            splitted_item = item.split("/")

            if len(splitted_item) > 5:
                is_secret_base = item.split("/")[-6] == "secret-base"
            else:
                is_secret_base = False

            try:
                if not is_secret_base:
                    blog_content["slug"] = slug
                    blog_content["category"] = "MLB"
                    blog_content["title"] = self.driver.find_element(
                        by=By.CSS_SELECTOR,
                        value='h1[class="c-page-title"]').get_attribute(
                        "innerHTML")
                    try:
                        blog_content["image_url"] = self.driver.find_element(
                            by=By.CSS_SELECTOR,
                            value='img[loading="eager"]').get_attribute("src")
                    except:
                        pass
                    blog_content["detail"] = self.driver.find_element(
                        by=By.CSS_SELECTOR,
                        value='div[class="c-entry-content "]'
                    ).get_attribute("innerHTML")
                    self.collection.append(blog_content)
                    with open("collection.json", "w") as file:
                        file.write(json.dumps(self.collection))


            except Exception as a:
                print(a)
                pass
