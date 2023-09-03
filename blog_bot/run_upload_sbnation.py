import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from blog_bot.upload_sbnation import create_blog_post

BASE_URL = "https://www.google.com"


class UploadSBNationBlogs:
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
        super(UploadSBNationBlogs, self).__init__()

    def __enter__(self):
        self.driver.get(BASE_URL)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.driver.quit()

    def land_first_page(self):
        self.driver.get(BASE_URL)

    def get_details(self):
        """
        this is used to get the detail links of all page
        :return:
        """
        # Read the JSON file
        with open('links.json', 'r') as file:
            data = json.load(file)

        # Process links one by one
        for link in data:
            try:
                print(f"Processing link: {link}")

                # Perform your processing here
                self.driver.get(link)
                # Find the unwanted elements by class name
                unwanted_elements = self.driver.find_elements(
                    by=By.CLASS_NAME,
                    value='metabet-adtile-auto'
                )
                # Remove unwanted elements from the DOM
                for element in unwanted_elements:
                    self.driver.execute_script("arguments[0].remove();", element)

                try:
                    title = self.driver.find_element(
                        by=By.CSS_SELECTOR,
                        value='h1[class="c-page-title"]').get_attribute(
                        "innerHTML")
                    image_url = None
                    try:
                        image_url = self.driver.find_element(
                            by=By.CSS_SELECTOR,
                            value='img[loading="eager"]').get_attribute("src")
                    except:
                        pass
                    detail = self.driver.find_element(
                        by=By.CSS_SELECTOR,
                        value='div[class="c-entry-content "]'
                    ).get_attribute("innerHTML")
                    # create blog post
                    if image_url:
                        create_blog_post(title, detail, image_url)
                except Exception as a:
                    print(a)
                    pass
                # Remove the processed link
                data.remove(link)

                # Update the JSON file
                with open('links.json', 'w') as file:
                    json.dump(data, file, indent=2)
            except Exception as a:
                print(a)


try:
    bot = UploadSBNationBlogs(teardown=True)
    bot.land_first_page()
    bot.get_details()
    print("Exiting")

except Exception as a:
    print(a)
