from LLM import generate_post, call_openai
from X_utils import post_tweet
from google_image import telecharger_image_album

from playwright.sync_api import sync_playwright

def download_html(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state('networkidle')
        html_content = page.content()
        browser.close()
        return html_content

def main():
    url = "https://www.allmusic.com/newreleases"
    rendered_html = download_html(url)
    print(rendered_html)
    tweet = generate_post(rendered_html, max_length=280)
    print(tweet)
    messages = [
        {"role": "user", "content": f"there is a tweet : {tweet} give me the title of the album/song and the artist. Your answer should be in the format : title by artist, nothing else"}
    ]
    artist_and_title = call_openai(messages)
    image_path = telecharger_image_album(artist_and_title)
    post_tweet(tweet, image_path=image_path)