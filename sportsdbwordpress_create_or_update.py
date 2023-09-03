import requests
from decouple import config
from bs4 import BeautifulSoup

# Replace these values with your WordPress site's information
wordpress_base_url = 'https://sportdatebook.com/wp-json/wp/v2'
jwt_token = config('JWT_TOKEN')


def upload_image(image_url):
    """
    this is used to upload an image
    :param image_url:
    :return:
    """
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
def get_category_id(category_slug):
    """
    this is used to get all categories
    :param category_slug:
    :return:
    """
    categories_endpoint = f'{wordpress_base_url}/categories'
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Content-Type': 'application/json',
    }
    response = requests.get(categories_endpoint, headers=headers)
    categories = response.json()

    for category in categories:
        if category["slug"] == category_slug:
            return category['id']
    return None


# Create a new blog post
def create_blog_post(title, content, image_url, slug, category_slug):
    """
    This function is used to create a post on WordPress.
    :param title: Title of the post.
    :param content: Content of the post.
    :param image_url: URL of the featured image.
    :param slug: Slug for the post.
    :param category_slug: Name of the category for the post.
    :return: Created post data if successful, None otherwise.
    """
    image_id = upload_image(image_url)

    category_id = get_category_id(category_slug)
    if not category_id:
        print(f"Category '{category_slug}' not found.")
        return

    endpoint = f'{wordpress_base_url}/posts'
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Content-Type': 'application/json',
    }
    if not image_id:
        data = {
            'title': title,
            'content': content,
            'status': 'publish',  # You can adjust the status (draft, pending, publish, etc.)
            'slug': slug,
            'categories': [category_id],
        }
    else:
        data = {
            'title': title,
            'content': content,
            'featured_media': image_id,
            'status': 'publish',  # You can adjust the status (draft, pending, publish, etc.)
            'slug': slug,
            'categories': [category_id],
        }

    response = requests.post(endpoint, headers=headers, json=data)

    if response.status_code == 201:
        print(slug)
        print("created")
        return response.json()
    else:
        print(f"Error creating blog post: {response.status_code}")
        print(response.text)
        return None


# Delete a blog post by ID
def delete_blog_post(post_id):
    """
    this is used to delete a post
    :param post_id:
    :return:
    """
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


def update_blog_post(post_id, title, content, image_url):
    """
    This function updates an existing blog post.
    :param post_id: ID of the post to be updated
    :param title: New title for the post
    :param content: New content for the post
    :param image_url: New image URL for the post
    :return: Updated post data if successful, None otherwise
    """
    image_id = upload_image(image_url)

    endpoint = f'{wordpress_base_url}/posts/{post_id}'
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Content-Type': 'application/json',
    }
    if not image_id:

        data = {
            'title': title,
            'content': content,
        }
    else:
        data = {
            'title': title,
            'content': content,
            'featured_media': image_id,
        }

    response = requests.put(endpoint, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error updating blog post: {response.status_code}")
        print(response.text)
        return None


def check_blog_post_exist(slug):
    """
    This function checks if a blog post exists based on its slug.
    :param slug: Slug of the post to be checked
    :return: True if the post exists, False otherwise
    """
    endpoint = f'{wordpress_base_url}/posts'
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Content-Type': 'application/json',
    }
    params = {
        'slug': slug,
    }

    response = requests.get(endpoint, headers=headers, params=params)

    if response.status_code == 200:
        if len(response.json()) == 0:
            return None
        post_data = response.json()[0]["id"]
        if post_data:
            return post_data
        else:
            return None
    else:
        print(f"Error checking blog post existence: {response.status_code}")
        print(response.text)
        return None


def create_or_update_blog_post(title, content, image_url, slug, category_slug):
    """
    This function creates a new blog post or updates an existing one based on slug existence.
    :param title: Title of the post.
    :param content: Content of the post.
    :param image_url: URL of the featured image.
    :param slug: Slug for the post.
    :param category_slug: Category slug for the post.
    :return: Created or updated post data if successful, None otherwise.
    """
    post_id = check_blog_post_exist(slug)

    if post_id:
        # Post exists, update it
        return True
        # return update_blog_post(post_id, title, content, image_url)
    else:
        # Post doesn't exist, create it
        return create_blog_post(title, content, image_url, slug, category_slug)


# # check_blog_post_exist("feed-2")
# for i in range(391,1000):
#     delete_blog_post(i)


def update_blog_post_domain(post_id):
    """
    This function updates the domain in the anchor tags of a blog post's content.
    :param post_id: ID of the post to be updated
    :param new_domain: New domain to replace in the anchor tags
    :param jwt_token: JWT token for authentication
    :return: True if the update was successful, False otherwise
    """
    endpoint = f'{wordpress_base_url}/posts/{post_id}'
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Content-Type': 'application/json',
    }

    response = requests.get(endpoint, headers=headers)

    if response.status_code == 200:
        post_data = response.json()
        if 'content' in post_data:
            content = post_data['content']['rendered']
            soup = BeautifulSoup(content, 'html.parser')

            # Find all anchor tags and update their 'href' attributes
            for a_tag in soup.find_all('a'):
                if 'href' in a_tag.attrs:
                    old_href = a_tag['href']
                    new_href = old_href.replace('https://playoffsschedule.com/', "https://sportdatebook.com/")
                    a_tag['href'] = new_href

            updated_content = str(soup)

            updated_data = {
                'content': updated_content
            }

            update_response = requests.post(endpoint, headers=headers, json=updated_data)
            print(updated_content)

            if update_response.status_code == 200:
                return True
            else:
                print(f"Error updating blog post content: {update_response.status_code}")
                print(update_response.text)
                return False
        else:
            print("Content not found in post data")
            return False
    else:
        print(f"Error getting blog post data: {response.status_code}")
        print(response.text)
        return False


def update_all_post_domains(new_domain):
    """
    This function updates anchor tags in all available posts' content.
    :param base_url: Base URL of the WordPress site's API
    :param jwt_token: JWT token for authentication
    :param new_domain: New domain to replace in anchor tags
    """

    # Function implementation (as shown in the previous responses)

    # Get the list of all posts
    posts_endpoint = f'{wordpress_base_url}/posts'
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Content-Type': 'application/json',
    }

    all_posts = []
    page = 1

    while True:
        response = requests.get(posts_endpoint, headers=headers, params={'page': page})
        page_posts = response.json()
        if response.status_code != 200:
            break
        all_posts.extend(page_posts)

        if not page_posts:
            break

        page += 1

    # Loop through posts and update anchor tags
    for post in all_posts:
        post_id = post['id']
        success = update_blog_post_domain(post_id)

        if success:
            print(f"Updated post {post_id} successfully")
        else:
            print(f"Failed to update post {post_id}")

# update_all_post_domains("https://sportdatebook.com/")
#
# check_blog_post_exist("virginia-cavaliers-schedule")

# print(update_blog_post_domain(689))
