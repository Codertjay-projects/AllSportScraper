import requests
from decouple import config

# Replace these values with your WordPress site's information
wordpress_base_url = 'https://sportdatebook.com/wp-json/wp/v2'
jwt_token = config('JWT_TOKEN')


def upload_image(image_url):
    if not image_url:
        return None
    endpoint = f'{wordpress_base_url}/media'
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Content-Type': 'image/jpeg',  # Replace with the correct image content type
        'Content-Disposition': 'attachment; filename=image.jpg',  # Provide a filename
    }
    image_data = requests.get(image_url).content
    response = requests.post(endpoint, headers=headers, data=image_data)

    if response.status_code == 201:
        return response.json()['id']
    else:
        print(f"Error uploading image: {response.status_code}")
        print(response.text)
        return None


# Fetch category IDs
def get_category_id(category_name):
    categories_endpoint = f'{wordpress_base_url}/categories'
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Content-Type': 'application/json',
    }
    response = requests.get(categories_endpoint, headers=headers)
    categories = response.json()

    for category in categories:
        if category['name'] == category_name:
            return category['id']
    return None


# Create a new blog post
def create_blog_post(title, content, image_url):
    image_id = upload_image(image_url)
    if not image_id:
        print("No image uploaded")
        return

    endpoint = f'{wordpress_base_url}/posts'
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Content-Type': 'application/json',
    }
    data = {
        'title': title,
        'content': content,
        'featured_media': image_id,
        'status': 'publish',  # You can adjust the status (draft, pending, publish, etc.)
    }

    response = requests.post(endpoint, headers=headers, json=data)

    if response.status_code == 201:

        return response.json()
    else:
        print(f"Error creating blog post: {response.status_code}")
        print(response.text)
        return None


# Delete a blog post by ID
def delete_blog_post(post_id):
    endpoint = f'{wordpress_base_url}/posts/{post_id}'
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Content-Type': 'application/json',
    }

    response = requests.delete(endpoint, headers=headers)

    if response.status_code == 200:
        print(f"Blog post with ID {post_id} deleted successfully!")
    else:
        print(f"Error deleting blog post: {response.status_code}")
        # print(response.text)


# Example usage
post_title = "Debugging"
post_content = """
\n
<div class="entry-content single-content">
<p>The Denver Nuggets defeated the Miami Heat 4-1 to become the champions of the 2023 NBA Finals on Monday, June 12, 2023.</p>
<p class="has-medium-font-size">2023 NBA Finals Winner</p>
<ul>
<li>Game 1: Nuggets 104, Heat 93</li>
<li>Game 2: Heat 111, Nuggets 108</li>
<li>Game 3: Nuggets 109, Heat 94</li>
<li>Game 4: Nuggets 108, Heat 95</li>
<li>Game 5: Nuggets 94, Heat 89</li>
</ul>
<figure class="wp-block-table"><table><thead><tr><th>YEAR</th><th>WINNER</th><th>OPPOSITION</th><th>SCORE</th></tr></thead><tbody><tr><td>2023</td><td>Denver Nuggets</td><td>Miami Heat</td><td>4-1</td></tr><tr><td>2022</td><td>Golden State Warriors</td><td>Boston Celtics</td><td>4-2</td></tr><tr><td>2021</td><td>Milwaukee Bucks</td><td>Phoenix Suns</td><td>4-2</td></tr><tr><td>2020</td><td>Los Angeles Lakers</td><td>Miami Heat</td><td>4-2</td></tr><tr><td>2019</td><td>Toronto Raptors</td><td>Golden State Warriors</td><td>4-2</td></tr><tr><td>2018</td><td>Golden State Warriors</td><td>Cleveland Cavaliers</td><td>4-0</td></tr><tr><td>2017</td><td>Golden State Warriors</td><td>Cleveland Cavaliers</td><td>4-1</td></tr><tr><td>2016</td><td>Cleveland Cavaliers</td><td>Golden State Warriors</td><td>4-3</td></tr><tr><td>2015</td><td>Golden State Warriors</td><td>Cleveland Cavaliers</td><td>4-2</td></tr><tr><td>2014</td><td>San Antonio Spurs</td><td>Miami Heat</td><td>4-1</td></tr><tr><td>2013</td><td>Miami Heat</td><td>San Antonio Spurs</td><td>4-3</td></tr><tr><td>2012</td><td>Miami Heat</td><td>Oklahoma City Thunder</td><td>4-1</td></tr><tr><td>2011</td><td>Dallas Mavericks</td><td>Miami Heat</td><td>4-2</td></tr><tr><td>2010</td><td>Los Angeles Lakers</td><td>Boston Celtic</td><td>4-3</td></tr><tr><td>2009</td><td>Los Angeles Lakers</td><td>Orlando Magic</td><td>4-1</td></tr><tr><td>2008</td><td>Boston Celtics</td><td>Los Angeles Lakers</td><td>4-2</td></tr><tr><td>2007</td><td>San Antonio Spurs</td><td>Cleveland Cavaliers</td><td>4-0</td></tr><tr><td>2006</td><td>Miami Heat</td><td>Dallas Mavericks</td><td>4-2</td></tr><tr><td>2005</td><td>San Antonio Spurs</td><td>Detroit Pistons</td><td>4-3</td></tr><tr><td>2004</td><td>Detroit Pistons</td><td>Los Angeles Lakers</td><td>4-1</td></tr><tr><td>2003</td><td>San Antonio Spurs</td><td>New Jersey Nets</td><td>4-2</td></tr><tr><td>2002</td><td>Los Angeles Lakers</td><td>New Jersey Nets</td><td>4-0</td></tr><tr><td>2001</td><td>Los Angeles Lakers</td><td>Philadelphia 76ers</td><td>4-1</td></tr><tr><td>2000</td><td>Los Angeles Lakers</td><td>Indiana Pacers</td><td>4-2</td></tr><tr><td>1999</td><td>San Antonio Spurs</td><td>New York Knicks</td><td>4-1</td></tr><tr><td>1998</td><td>Chicago Bulls</td><td>Utah Jazz</td><td>4-2</td></tr><tr><td>1997</td><td>Chicago Bulls</td><td>Utah Jazz</td><td>4-2</td></tr><tr><td>1996</td><td>Chicago Bulls</td><td>Seattle SuperSonics</td><td>4-2</td></tr><tr><td>1995</td><td>Houston Rockets</td><td>Orlando Magic</td><td>4-0</td></tr><tr><td>1994</td><td>Houston Rockets</td><td>New York Knicks</td><td>4-3</td></tr><tr><td>1993</td><td>Chicago Bulls</td><td>Phoenix Suns</td><td>4-2</td></tr><tr><td>1992</td><td>Chicago Bulls</td><td>Portland Trail Blazers</td><td>4-2</td></tr><tr><td>1991</td><td>Chicago Bulls</td><td>Los Angeles Lakers</td><td>4-1</td></tr><tr><td>1990</td><td>Detroit Pistons</td><td>Portland Trail Blazers</td><td>4-1</td></tr><tr><td>1989</td><td>Detroit Pistons</td><td>Los Angeles Lakers</td><td>4-0</td></tr><tr><td>1988</td><td>Los Angeles Lakers</td><td>Detroit Pistons</td><td>4-3</td></tr><tr><td>1987</td><td>Los Angeles Lakers</td><td>Boston Celtics</td><td>4-2</td></tr><tr><td>1986</td><td>Boston Celtics</td><td>Houston Rockets</td><td>4-2</td></tr><tr><td>1985</td><td>Los Angeles Lakers</td><td>Boston Celtics</td><td>4-2</td></tr><tr><td>1984</td><td>Boston Celtics</td><td>Los Angeles Lakers</td><td>4-3</td></tr><tr><td>1983</td><td>Philadelphia 76ers</td><td>Los Angeles Lakers</td><td>4-0</td></tr><tr><td>1982</td><td>Los Angeles Lakers</td><td>Philadelphia 76ers</td><td>4-2</td></tr><tr><td>1981</td><td>Boston Celtics</td><td>Houston Rockets</td><td>4-2</td></tr><tr><td>1980</td><td>Los Angeles Lakers</td><td>Philadelphia 76ers</td><td>4-2</td></tr><tr><td>1979</td><td>Seattle SuperSonics</td><td>Washington Bullets</td><td>4-1</td></tr><tr><td>1978</td><td>Washington Bullets</td><td>Seattle SuperSonics</td><td>4-3</td></tr><tr><td>1977</td><td>Portland Trail Blazers</td><td>Philadelphia 76ers</td><td>4-2</td></tr><tr><td>1976</td><td>Boston Celtics</td><td>Phoenix Suns</td><td>4-2</td></tr><tr><td>1975</td><td>Golden State Warriors</td><td>Washington Bullets</td><td>4-0</td></tr><tr><td>1974</td><td>Boston Celtics</td><td>Milwaukee Bucks</td><td>4-3</td></tr><tr><td>1973</td><td>New York Knicks</td><td>Los Angeles Lakers</td><td>4-1</td></tr><tr><td>1972</td><td>Los Angeles Lakers</td><td>New York Knicks</td><td>4-1</td></tr><tr><td>1971</td><td>Milwaukee Bucks</td><td>Baltimore Bullets</td><td>4-0</td></tr><tr><td>1970</td><td>New York Knicks</td><td>Los Angeles Lakers</td><td>4-3</td></tr><tr><td>1969</td><td>Boston Celtics</td><td>Los Angeles Lakers</td><td>4-3</td></tr><tr><td>1968</td><td>Boston Celtics</td><td>Los Angeles Lakers</td><td>4-2</td></tr><tr><td>1967</td><td>Philadelphia 76ers</td><td>San Francisco Warriors</td><td>4-2</td></tr><tr><td>1966</td><td>Boston Celtics</td><td>Los Angeles Lakers</td><td>4-3</td></tr><tr><td>1965</td><td>Boston Celtics</td><td>Los Angeles Lakers</td><td>4-1</td></tr><tr><td>1964</td><td>Boston Celtics</td><td>San Francisco Warriors</td><td>4-1</td></tr><tr><td>1963</td><td>Boston Celtics</td><td>Los Angeles Lakers</td><td>4-2</td></tr><tr><td>1962</td><td>Boston Celtics</td><td>Los Angeles Lakers</td><td>4-3</td></tr><tr><td>1961</td><td>Boston Celtics</td><td>St. Louis Hawks</td><td>4-1</td></tr><tr><td>1960</td><td>Boston Celtics</td><td>St. Louis Hawks</td><td>4-3</td></tr><tr><td>1959</td><td>Boston Celtics</td><td>Minneapolis Lakers</td><td>4-0</td></tr><tr><td>1958</td><td>St. Louis Hawks</td><td>Boston Celtics</td><td>4-2</td></tr><tr><td>1957</td><td>Boston Celtics</td><td>St. Louis Hawks</td><td>4-3</td></tr><tr><td>1956</td><td>Philadelphia Warriors</td><td>Fort Wayne Pistons</td><td>4-1</td></tr><tr><td>1955</td><td>Syracuse Nationals</td><td>Fort Wayne Pistons</td><td>4-3</td></tr><tr><td>1954</td><td>Minneapolis Lakers</td><td>Syracuse Nationals</td><td>4-3</td></tr><tr><td>1953</td><td>Minneapolis Lakers</td><td>New York Knicks</td><td>4-1</td></tr><tr><td>1952</td><td>Minneapolis Lakers</td><td>New York Knicks</td><td>4-3</td></tr><tr><td>1951</td><td>Rochester Royals</td><td>New York Knicks</td><td>4-3</td></tr><tr><td>1950</td><td>Minneapolis Lakers</td><td>Syracuse Nationals</td><td>4-2</td></tr><tr><td>1949</td><td>Minneapolis Lakers</td><td>Washington Capitols</td><td>4-2</td></tr><tr><td>1948</td><td>Baltimore Bullets</td><td>Philadelphia Warriors</td><td>4-2</td></tr><tr><td>1947</td><td>Philadelphia Warriors</td><td>Chicago Stags</td><td>4-1</td></tr></tbody></table></figure>
</div>
"""
# for item in range(117,500):
#     delete_blog_post(item)
#
image_url = "https://ichef.bbci.co.uk/onesport/cps/624/cpsprodpb/159B9/production/_114750588_0.generic_done_deal-1.png"
new_post = create_blog_post(post_title, post_content, image_url)
if new_post:
    print("New blog post created successfully!")
    print(f"Post ID: {new_post['id']}")
