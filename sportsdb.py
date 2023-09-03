"""
This is used to make a post request to update or create transfer
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager

from open_api import transform_text, transform_title
from sportsdbwordpress_create_or_update import create_or_update_blog_post, check_blog_post_exist

BASE_URL = "https://www.thesportsdb.com/transfers_latest.php"


class TheSportsDB:
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
        self.detail_links = []
        self.page_detail_links = []
        self.driver.implicitly_wait(50)
        super(TheSportsDB, self).__init__()

    def __enter__(self):
        self.driver.get(BASE_URL)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.driver.quit()

    def land_first_page(self):
        self.driver.get(BASE_URL)

    def get_latest_transfers(self):
        """
        this is used to get the detail links of all page
        :return:
        """
        self.driver.get("https://www.thesportsdb.com/transfers_latest.php")
        # Find all image elements within the table
        image_elements = self.driver.find_elements(By.TAG_NAME, "img")
        link_elements = self.driver.find_elements(By.TAG_NAME, "a")

        # Loop through the image elements and modify their src attributes
        for img_element in image_elements:
            src = img_element.get_attribute("src")
            self.driver.execute_script("arguments[0].setAttribute('src', arguments[1])", img_element, src)

        # Loop through the image elements and modify their src attributes
        counter = 0
        for link_element in link_elements:
            counter += 1
            if counter <= 2:
                link_style = 'display:none;'
                self.driver.execute_script("arguments[0].setAttribute('style', arguments[1])", link_element, link_style)
            self.driver.execute_script("arguments[0].setAttribute('href', arguments[1])", link_element, "#")

        # Capture the outerHTML of the table after making changes to the src attributes
        table_element = self.driver.find_element(by=By.TAG_NAME, value="table")
        table_element_style = ' border-collapse: collapse;'
        self.driver.execute_script("arguments[0].setAttribute('style', arguments[1])", table_element,
                                   table_element_style)
        content = self.driver.find_element(by=By.TAG_NAME, value='table').get_attribute(
            "outerHTML")

        image_url = "https://images.sportsbrief.com/images/1120/0c2a0fdc6824392b.jpeg?v=1"
        title = transform_title("Latest Transfers")
        slug = "transfers-latest"
        print(title)

        _ = create_or_update_blog_post(title, content, image_url, slug, "informational-nuggets")

    def get_players_birthday(self):
        """
        this is used to get the detail links of all page
        :return:
        """
        self.driver.get("https://thesportsdb.com/player_birthday.php")
        # Find all image elements within the table
        image_elements = self.driver.find_elements(By.TAG_NAME, "img")
        link_elements = self.driver.find_elements(By.TAG_NAME, "a")

        # Loop through the image elements and modify their src attributes
        for img_element in image_elements:
            src = img_element.get_attribute("src")
            self.driver.execute_script("arguments[0].setAttribute('src', arguments[1])", img_element, src)

        # Loop through the image elements and modify their src attributes
        for link_element in link_elements:
            self.driver.execute_script("arguments[0].setAttribute('href', arguments[1])", link_element, "#")

        # Capture the outerHTML of the table after making changes to the src attributes
        table_element = self.driver.find_element(by=By.TAG_NAME, value="table")
        table_element_style = ' border-collapse: collapse;'
        self.driver.execute_script("arguments[0].setAttribute('style', arguments[1])", table_element,
                                   table_element_style)
        content = self.driver.find_element(by=By.CSS_SELECTOR, value='div[class="col-sm-10"]').get_attribute(
            "outerHTML")

        image_url = "https://assets.goal.com/v3/assets/bltcc7a7ffd2fbf71f5/bltf352a5d3475862c2/60de17785775160f9f2ae8c5/7ef8432a64e59f78c3175dbbb7a03854690af7f7.jpg?auto=webp&format=pjpg&width=1080&quality=60"
        title = transform_title("Born on this day")
        slug = "player-birthday"
        print(title)
        _ = create_or_update_blog_post(title, content, image_url, slug, "informational-nuggets")

    def get_latest_honors(self):
        self.driver.get("https://thesportsdb.com/honour_latest.php")
        """
        this is used to get the detail links of all page
        :return:
        """
        # Find all image elements within the table
        image_elements = self.driver.find_elements(By.TAG_NAME, "img")
        link_elements = self.driver.find_elements(By.TAG_NAME, "a")

        # Loop through the image elements and modify their src attributes
        for img_element in image_elements:
            src = img_element.get_attribute("src")
            self.driver.execute_script("arguments[0].setAttribute('src', arguments[1])", img_element, src)

        # Loop through the image elements and modify their src attributes
        counter = 0
        for link_element in link_elements:
            counter += 1
            if counter <= 2:
                link_style = 'display:none;'
                self.driver.execute_script("arguments[0].setAttribute('style', arguments[1])", link_element, link_style)
            self.driver.execute_script("arguments[0].setAttribute('href', arguments[1])", link_element, "#")

        # Capture the outerHTML of the table after making changes to the src attributes
        table_element = self.driver.find_element(by=By.TAG_NAME, value="table")
        table_element_style = ' border-collapse: collapse;'
        self.driver.execute_script("arguments[0].setAttribute('style', arguments[1])", table_element,
                                   table_element_style)
        content = self.driver.find_element(by=By.TAG_NAME, value='table').get_attribute(
            "outerHTML")

        image_url = "https://besthqwallpapers.com/Uploads/11-12-2021/187293/thumb2-3d-fifa-world-cup-4k-yellow-brickwall-creative-football-trophies.jpg"
        title = transform_title("Latest Honours")
        slug = "honour-latest"
        print(title)

        _ = create_or_update_blog_post(title, content, image_url, slug, "informational-nuggets")

    def get_latest_stats(self):
        self.driver.get("https://thesportsdb.com/stats_center.php")
        """
        this is used to get the detail links of all page
        :return:
        """
        # Find all image elements within the table
        image_elements = self.driver.find_elements(By.TAG_NAME, "img")
        link_elements = self.driver.find_elements(By.TAG_NAME, "a")

        # Loop through the image elements and modify their src attributes
        for img_element in image_elements:
            src = img_element.get_attribute("src")
            self.driver.execute_script("arguments[0].setAttribute('src', arguments[1])", img_element, src)

        # Loop through the image elements and modify their src attributes
        counter = 0
        for link_element in link_elements:
            counter += 1
            if counter <= 2:
                link_style = 'display:none;'
                self.driver.execute_script("arguments[0].setAttribute('style', arguments[1])", link_element, link_style)
            self.driver.execute_script("arguments[0].setAttribute('href', arguments[1])", link_element, "#")

        # Capture the outerHTML of the table after making changes to the src attributes
        table_element = self.driver.find_element(by=By.TAG_NAME, value="table")
        table_element_style = ' border-collapse: collapse;'
        self.driver.execute_script("arguments[0].setAttribute('style', arguments[1])", table_element,
                                   table_element_style)
        content = self.driver.find_elements(by=By.TAG_NAME, value='table')[-1].get_attribute(
            "outerHTML")

        image_url = "https://blog.statscore.com/wp-content/uploads/2020/11/Stats.jpg"
        title = transform_title("Latest Player Statistics")
        slug = "stats-center"
        print(title)

        _ = create_or_update_blog_post(title, content, image_url, slug, "informational-nuggets")

    def get_feeds(self):
        self.driver.get("https://thesportsdb.com/feed")
        """
        this is used to get the detail links of all page
        :return:
        """
        # Find all image elements within the table
        image_elements = self.driver.find_elements(By.TAG_NAME, "img")
        link_elements = self.driver.find_elements(By.TAG_NAME, "a")

        # Loop through the image elements and modify their src attributes
        for img_element in image_elements:
            src = img_element.get_attribute("src")
            self.driver.execute_script("arguments[0].setAttribute('src', arguments[1])", img_element, src)

        # Loop through the image elements and modify their src attributes
        for link_element in link_elements:
            self.driver.execute_script("arguments[0].setAttribute('href', arguments[1])", link_element, "#")

        # Capture the outerHTML of the table after making changes to the src attributes
        table_element = self.driver.find_element(by=By.TAG_NAME, value="table")
        table_element_style = ' border-collapse: collapse;'
        self.driver.execute_script("arguments[0].setAttribute('style', arguments[1])", table_element,
                                   table_element_style)
        content = self.driver.find_elements(by=By.CSS_SELECTOR, value='div[class="row"]')[-2].get_attribute(
            "outerHTML")

        image_url = "https://img.freepik.com/free-photo/sports-tools_53876-138077.jpg?w=2000"
        title = transform_title("Recent Activity")
        slug = "feed-2"
        print(title)

        _ = create_or_update_blog_post(title, content, image_url, slug, "informational-nuggets")

    def get_hall_of_fame_players(self):
        self.driver.get("https://thesportsdb.com/hall_of_fame_player.php")
        """
        this is used to get the detail links of all page
        :return:
        """
        # Find all image elements within the table
        image_elements = self.driver.find_elements(By.TAG_NAME, "img")
        link_elements = self.driver.find_elements(By.TAG_NAME, "a")

        # Loop through the image elements and modify their src attributes
        for img_element in image_elements:
            src = img_element.get_attribute("src")
            self.driver.execute_script("arguments[0].setAttribute('src', arguments[1])", img_element, src)

        # Loop through the image elements and modify their src attributes
        for link_element in link_elements:
            self.driver.execute_script("arguments[0].setAttribute('href', arguments[1])", link_element, "#")

        # Capture the outerHTML of the table after making changes to the src attributes
        table_element = self.driver.find_element(by=By.TAG_NAME, value="table")
        table_element_style = ' border-collapse: collapse;'
        self.driver.execute_script("arguments[0].setAttribute('style', arguments[1])", table_element,
                                   table_element_style)
        content = self.driver.find_element(by=By.TAG_NAME, value='table').get_attribute(
            "outerHTML")

        image_url = "https://sportal365images.com/process/smp-images-production/ringier.africa/11052023/f47d9cda-f3d2-4ce0-9719-a1e7214695db.png?operations=fit(960:)"
        title = transform_title("Player Hall of Fame (All Sports)")
        slug = "hall-of-fame-player"
        print(title)

        _ = create_or_update_blog_post(title, content, image_url, slug, "informational-nuggets")

    def get_top_hundred_events_of_all_time(self):
        self.driver.get("https://thesportsdb.com/top100.php")
        """
        this is used to get the detail links of all page
        :return:
        """
        # Find all image elements within the table
        image_elements = self.driver.find_elements(By.TAG_NAME, "img")
        link_elements = self.driver.find_elements(By.TAG_NAME, "a")

        # Loop through the image elements and modify their src attributes
        for img_element in image_elements:
            src = img_element.get_attribute("src")
            self.driver.execute_script("arguments[0].setAttribute('src', arguments[1])", img_element, src)

        # Loop through the image elements and modify their src attributes
        for link_element in link_elements:
            self.driver.execute_script("arguments[0].setAttribute('href', arguments[1])", link_element, "#")

        # Capture the outerHTML of the table after making changes to the src attributes
        table_element = self.driver.find_element(by=By.TAG_NAME, value="table")
        table_element_style = ' border-collapse: collapse;'
        self.driver.execute_script("arguments[0].setAttribute('style', arguments[1])", table_element,
                                   table_element_style)
        content = self.driver.find_element(by=By.CSS_SELECTOR, value='div[class="col-sm-10"]').get_attribute(
            "outerHTML")
        image_url = "https://i0.wp.com/www.wonderslist.com/wp-content/uploads/2012/09/The-FIFA-World-Cup.jpg"
        title = transform_title("Top Events of all time as rated by our users")
        slug = "top-100"
        print(title)

        _ = create_or_update_blog_post(title, content, image_url, slug, "informational-nuggets")

    def get_play_off_posts(self):
        self.driver.get("https://playoffsschedule.com/")
        all_detail_links = self.driver.find_elements(by=By.CSS_SELECTOR, value='a[rel="bookmark"]')
        # get all the detail links
        for item in all_detail_links:
            self.detail_links.append(item.get_attribute("href"))
        for item in self.detail_links:
            self.get_play_off_schedule_detail(item, "informational-nuggets")

    def get_page_detail_links(self):
        item_count = 0

        while True:
            item_count += 1
            if item_count == 1:
                self.driver.get("https://playoffsschedule.com/?s=a")
            else:
                self.driver.get(f"https://playoffsschedule.com/page/{item_count}/?s=a")
            try:
                all_detail_links = self.driver.find_elements(by=By.CSS_SELECTOR, value='a[rel="bookmark"]')
                if len(all_detail_links) == 0:
                    return
                    # get all the detail links
                for link_item in all_detail_links:
                    self.page_detail_links.append(link_item.get_attribute("href"))
            except Exception as e:
                print(e)
                return

    def get_play_off_posts_with_search(self):
        self.get_page_detail_links()
        try:
            for link_item in self.page_detail_links:
                self.get_play_off_schedule_detail(link_item, "informational-nuggets")
        except Exception as e:
            print(e)
            return

    def get_play_off_schedule_detail(self, link, category):
        """
        this is used to get the nba finals full list
        :return:
        """
        slug = link.split("/")[-2]
        # check if slug exist
        post_id = check_blog_post_exist(slug)
        if post_id:
            print("post exists")
            return
        try:
            self.driver.get(link)
            self.replace_all_a_tags()
            paragraphs = self.driver.find_elements(by=By.CSS_SELECTOR,
                                                   value='div[class="entry-content single-content"] p')[
                         :3]
            for paragraph in paragraphs:
                original_content = paragraph.get_attribute("outerHTML")
                transformed_content = transform_text(original_content)
                self.driver.execute_script(f'arguments[0].outerHTML = `{transformed_content}`;', paragraph)
            unordered_lists = self.driver.find_elements(by=By.CSS_SELECTOR,
                                                        value='div[class="entry-content single-content"] ul')[:3]
            for unordered_list in unordered_lists:
                original_content = unordered_list.get_attribute("outerHTML")
                transformed_content = transform_text(original_content)
                self.driver.execute_script(f'arguments[0].outerHTML = `{transformed_content}`;', unordered_list)

            content = self.driver.find_element(by=By.CSS_SELECTOR,
                                               value='div[class="entry-content single-content"]').get_attribute(
                "outerHTML")
            title = transform_title(
                self.driver.find_element(by=By.CSS_SELECTOR, value='h1[class="entry-title"]').get_attribute(
                    "innerHTML"))
            try:
                image_url = self.driver.find_element(by=By.CSS_SELECTOR,
                                                     value='div[class="post-thumbnail-inner"]').find_element(
                    by=By.TAG_NAME,
                    value='img'). \
                    get_attribute("src")
            except:
                image_url = None
            slug = link.split("/")[-2]
            if slug == "contact-us":
                return
            print(title)
            _ = create_or_update_blog_post(title, content, image_url, slug, category)
        except Exception as a:
            print("error on detail scraping: ", a)
            pass

    def get_nba_play_off_schedule(self):
        """
        this is used to get nba play off schedule
        :return:
        """

        self.driver.get("https://playoffsschedule.com/nba-playoff-schedule/")
        self.replace_all_a_tags()
        paragraphs = self.driver.find_elements(by=By.CSS_SELECTOR, value='div[class="entry-content single-content"] p')[
                     :3]
        for paragraph in paragraphs:
            original_content = paragraph.get_attribute("outerHTML")
            transformed_content = transform_text(original_content)
            self.driver.execute_script(f'arguments[0].outerHTML = `{transformed_content}`;', paragraph)
        unordered_lists = self.driver.find_elements(by=By.CSS_SELECTOR,
                                                    value='div[class="entry-content single-content"] ul')[:3]
        for unordered_list in unordered_lists:
            original_content = unordered_list.get_attribute("outerHTML")
            transformed_content = transform_text(original_content)
            self.driver.execute_script(f'arguments[0].outerHTML = `{transformed_content}`;', unordered_list)

        content = self.driver.find_element(by=By.CSS_SELECTOR,
                                           value='div[class="entry-content single-content"]').get_attribute("outerHTML")
        title = transform_title(
            self.driver.find_element(by=By.CSS_SELECTOR, value='h1[class="entry-title"]').get_attribute("innerHTML"))
        image_url = "https://library.sportingnews.com/2023-06/NBA%20Playoffs%20Bracket%20060123.jpg"
        slug = "nba-play-off-schedule"
        _ = create_or_update_blog_post(title, content, image_url, slug, "playoffs-schedule")

    def get_nfl_play_off_schedule(self):
        """
        this is used to get nba play off schedule
        :return:
        """

        self.driver.get("https://playoffsschedule.com/nfl-playoff-schedule/")
        self.replace_all_a_tags()
        paragraphs = self.driver.find_elements(by=By.CSS_SELECTOR, value='div[class="entry-content single-content"] p')[
                     :3]
        for paragraph in paragraphs:
            original_content = paragraph.get_attribute("outerHTML")
            transformed_content = transform_text(original_content)
            self.driver.execute_script(f'arguments[0].outerHTML = `{transformed_content}`;', paragraph)
        unordered_lists = self.driver.find_elements(by=By.CSS_SELECTOR,
                                                    value='div[class="entry-content single-content"] ul')[:3]
        for unordered_list in unordered_lists:
            original_content = unordered_list.get_attribute("outerHTML")
            transformed_content = transform_text(original_content)
            self.driver.execute_script(f'arguments[0].outerHTML = `{transformed_content}`;', unordered_list)

        content = self.driver.find_element(by=By.CSS_SELECTOR,
                                           value='div[class="entry-content single-content"]').get_attribute("outerHTML")
        title = transform_title(
            self.driver.find_element(by=By.CSS_SELECTOR, value='h1[class="entry-title"]').get_attribute("innerHTML"))
        image_url = "https://www.profootballnetwork.com/wp-content/uploads/2023/01/2023-Divisional-Round-Bracket.png"
        slug = "nfl-play-off-schedule"
        print(title)

        _ = create_or_update_blog_post(title, content, image_url, slug, "playoffs-schedule")

    def get_ncaa_play_off_schedule(self):
        """
        this is used to get nba play off schedule
        :return:
        """

        self.driver.get("https://playoffsschedule.com/college-football-playoff-schedule/")
        self.replace_all_a_tags()
        paragraphs = self.driver.find_elements(by=By.CSS_SELECTOR, value='div[class="entry-content single-content"] p')[
                     :3]
        for paragraph in paragraphs:
            original_content = paragraph.get_attribute("outerHTML")
            transformed_content = transform_text(original_content)
            self.driver.execute_script(f'arguments[0].outerHTML = `{transformed_content}`;', paragraph)
        unordered_lists = self.driver.find_elements(by=By.CSS_SELECTOR,
                                                    value='div[class="entry-content single-content"] ul')[:3]
        for unordered_list in unordered_lists:
            original_content = unordered_list.get_attribute("outerHTML")
            transformed_content = transform_text(original_content)
            self.driver.execute_script(f'arguments[0].outerHTML = `{transformed_content}`;', unordered_list)

        content = self.driver.find_element(by=By.CSS_SELECTOR,
                                           value='div[class="entry-content single-content"]').get_attribute("outerHTML")
        title = transform_title(
            self.driver.find_element(by=By.CSS_SELECTOR, value='h1[class="entry-title"]').get_attribute("innerHTML"))
        image_url = "https://s.yimg.com/ny/api/res/1.2/qrBx07fuoy25te3VQvoksQ--/YXBwaWQ9aGlnaGxhbmRlcjtoPTY2Ng--/https://s.yimg.com/os/creatr-uploaded-images/2023-05/97312df0-e90e-11ed-91ff-fea97cfd8628"
        slug = "ncaa-play-off-schedule"
        print(title)

        _ = create_or_update_blog_post(title, content, image_url, slug, "playoffs-schedule")

    def get_mlb_play_off_schedule(self):
        """
        this is used to get nba play off schedule
        :return:
        """

        self.driver.get("https://playoffsschedule.com/college-football-playoff-schedule/")
        self.replace_all_a_tags()
        paragraphs = self.driver.find_elements(by=By.CSS_SELECTOR, value='div[class="entry-content single-content"] p')[
                     :3]
        for paragraph in paragraphs:
            original_content = paragraph.get_attribute("outerHTML")
            transformed_content = transform_text(original_content)
            self.driver.execute_script(f'arguments[0].outerHTML = `{transformed_content}`;', paragraph)
        unordered_lists = self.driver.find_elements(by=By.CSS_SELECTOR,
                                                    value='div[class="entry-content single-content"] ul')[:3]
        for unordered_list in unordered_lists:
            original_content = unordered_list.get_attribute("outerHTML")
            transformed_content = transform_text(original_content)
            self.driver.execute_script(f'arguments[0].outerHTML = `{transformed_content}`;', unordered_list)

        content = self.driver.find_element(by=By.CSS_SELECTOR,
                                           value='div[class="entry-content single-content"]').get_attribute("outerHTML")
        title = transform_title(
            self.driver.find_element(by=By.CSS_SELECTOR, value='h1[class="entry-title"]').get_attribute("innerHTML"))
        image_url = "https://img.mlbstatic.com/mlb-images/image/private/t_16x9/t_w1024/mlb/c0judjohje8dbby4muvv"
        slug = "mlb-play-off-schedule"
        print(title)

        _ = create_or_update_blog_post(title, content, image_url, slug, "playoffs-schedule")

    def get_nhl_play_off_schedule(self):
        """
        this is used to get nba play off schedule
        :return:
        """

        self.driver.get("https://playoffsschedule.com/nhl-playoff-schedule/")
        # Modify all p tags on the page with AI-generated content
        self.replace_all_a_tags()
        paragraphs = self.driver.find_elements(by=By.CSS_SELECTOR, value='div[class="entry-content single-content"] p')[
                     :3]
        for paragraph in paragraphs:
            original_content = paragraph.get_attribute("outerHTML")
            transformed_content = transform_text(original_content)
            self.driver.execute_script(f'arguments[0].outerHTML = `{transformed_content}`;', paragraph)
        unordered_lists = self.driver.find_elements(by=By.CSS_SELECTOR,
                                                    value='div[class="entry-content single-content"] ul')[:3]
        for unordered_list in unordered_lists:
            original_content = unordered_list.get_attribute("outerHTML")
            transformed_content = transform_text(original_content)
            self.driver.execute_script(f'arguments[0].outerHTML = `{transformed_content}`;', unordered_list)

        content = self.driver.find_element(by=By.CSS_SELECTOR,
                                           value='div[class="entry-content single-content"]').get_attribute("outerHTML")
        title = transform_title(
            self.driver.find_element(by=By.CSS_SELECTOR, value='h1[class="entry-title"]').get_attribute("innerHTML"))
        image_url = "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/21c5ee86-0e33-41fc-9a93-18279624dd66/dfum8x2-158f958d-77d4-4dd1-bb77-08f2dd5eabbe.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzIxYzVlZTg2LTBlMzMtNDFmYy05YTkzLTE4Mjc5NjI0ZGQ2NlwvZGZ1bTh4Mi0xNThmOTU4ZC03N2Q0LTRkZDEtYmI3Ny0wOGYyZGQ1ZWFiYmUucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.aEOaHbtMyJYx6G4C5mLxGduieJNDuW7OQHIRfMKdFy8"
        slug = "nhl-play-off-schedule"

        _ = create_or_update_blog_post(title, content, image_url, slug, "playoffs-schedule")

    def replace_all_a_tags(self):
        # Define the base domain you want to replace
        old_base_domain = "https://playoffsschedule.com"
        new_base_domain = "https://sportdatebook.com"

        # Find all <a> elements on the page
        all_links = self.driver.find_elements(By.TAG_NAME, "a")

        # Iterate through each link and modify the href attribute
        for link in all_links:
            href = link.get_attribute("href")
            if href and href.startswith(old_base_domain):
                new_href = href.replace(old_base_domain, new_base_domain)
                self.driver.execute_script(f'arguments[0].setAttribute("href", "{new_href}")', link)


try:
    bot = TheSportsDB(teardown=True)
    # bot.get_latest_transfers()
    # bot.get_players_birthday()
    # bot.get_latest_honors()
    # bot.get_hall_of_fame_players()
    # bot.get_top_hundred_events_of_all_time()
    # get the play off posts
    # bot.get_play_off_posts()
    bot.get_play_off_posts_with_search()
    # get play off schedule
    # bot.get_nba_play_off_schedule()
    # bot.get_nfl_play_off_schedule()
    # bot.get_ncaa_play_off_schedule()
    # bot.get_mlb_play_off_schedule()
    # bot.get_nhl_play_off_schedule()
    print("Exiting")

except Exception as a:
    print(a)
