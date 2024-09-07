# from playwright.sync_api import sync_playwright


# def scrape_profile(url: str) -> dict:
#     """
#     Scrape an X.com profile details, e.g.: https://x.com/Scrapfly_dev
#     """
#     _xhr_calls = []

#     def intercept_response(response):
#         """Capture all background requests and save them"""
#         # we can extract details from background requests
#         if response.request.resource_type == "xhr":
#             _xhr_calls.append(response)
#         return response

#     with sync_playwright() as pw:
#         browser = pw.chromium.launch(headless=False)  # Launches browser in non-headless mode
#         context = browser.new_context(viewport={"width": 1920, "height": 1080})
#         page = context.new_page()

#         # Enable background request intercepting:
#         page.on("response", intercept_response)
        
#         # Go to URL and wait for the page to load
#         page.goto(url)
#         page.wait_for_selector("[data-testid='primaryColumn']")

#         # Find all tweet background requests:
#         tweet_calls = [f for f in _xhr_calls if "UserBy" in f.url]
#         for xhr in tweet_calls:
#             data = xhr.json()
#             return data['data']['user']['result']

#     return {}


# if __name__ == "__main__":
#     # Run synchronously since sync_playwright is used
#     print(scrape_profile("https://x.com/elonmusk?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor"))



# from playwright.sync_api import sync_playwright
# import json

# def scrape_profile(url: str) -> dict:
#     """
#     Scrape an X.com profile details and fetch recent posts (tweets) and comments (replies).
#     """
#     _xhr_calls = []

#     def intercept_response(response):
#         """Capture all background requests (XHR) and save them"""
#         if response.request.resource_type == "xhr":
#             try:
#                 if "graphql" in response.url:
#                     _xhr_calls.append(response)
#             except Exception as e:
#                 print(f"Error while intercepting response: {e}")

#     with sync_playwright() as pw:
#         browser = pw.chromium.launch(headless=False)  # Launch browser in non-headless mode
#         context = browser.new_context(viewport={"width": 1920, "height": 1080})
#         page = context.new_page()

#         # Enable background request intercepting:
#         page.on("response", intercept_response)
        
#         # Go to the profile URL
#         page.goto(url)
#         page.wait_for_selector("[data-testid='primaryColumn']")  # Wait for profile to load

#         # Scroll down to load more tweets
#         for _ in range(5):  # Adjust range to load more tweets if needed
#             page.mouse.wheel(0, 3000)  # Scroll down by 3000 pixels
#             page.wait_for_timeout(2000)  # Wait for new tweets to load

#         # Filter relevant XHR requests that contain tweets data (GraphQL responses):
#         tweet_calls = [f for f in _xhr_calls if "UserTweets" in f.url or "TweetDetail" in f.url]
#         tweets = []

#         # Extract data from those GraphQL responses
#         for tweet_call in tweet_calls:
#             try:
#                 response_json = tweet_call.json()
#                 for instruction in response_json['data']['user']['result']['timeline_v2']['timeline']['instructions']:
#                     for entry in instruction.get('entries', []):
#                         tweet_result = entry.get('content', {}).get('itemContent', {}).get('tweet_results', {}).get('result', {})
#                         if tweet_result:
#                             tweet_legacy = tweet_result.get('legacy', {})
#                             tweets.append({
#                                 "id": tweet_result.get('rest_id'),
#                                 "text": tweet_legacy.get('full_text', ''),
#                                 "favorites": tweet_legacy.get('favorite_count', 0),
#                                 "retweets": tweet_legacy.get('retweet_count', 0),
#                             })
#             except Exception as e:
#                 print(f"Error processing tweet data: {e}")

#         return {"tweets": tweets}


# if __name__ == "__main__":
#     # Scrape the profile and print the result
#     profile_url = "https://x.com/elonmusk?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor"
#     profile_data = scrape_profile(profile_url)
#     print(json.dumps(profile_data, indent=2))





from playwright.sync_api import sync_playwright
import json
import os


def scrape_profile(url: str) -> dict:
    """
    Scrape an X.com profile details, fetch the post (tweet), and capture a screenshot.
    """
    _xhr_calls = []
    screenshot_dir = "tweet_screenshots"

    # Create directory for screenshots if it doesn't exist
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    def intercept_response(response):
        """Capture all background requests (XHR) and save them"""
        if response.request.resource_type == "xhr":
            _xhr_calls.append(response)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)  # Launch browser in non-headless mode
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        # Enable background request intercepting:
        page.on("response", intercept_response)
        
        # Go to the tweet URL
        page.goto(url)
        page.wait_for_selector("[data-testid='primaryColumn']")  # Wait for tweet to load

        # Wait for the tweet to appear on the page
        page.wait_for_timeout(3000)

        # Extract the first tweet and capture a screenshot
        tweet_element = page.query_selector(f'[data-testid="tweet"]')
        if tweet_element:
            tweet_text = tweet_element.text_content()
            tweet_id = url.split('/')[-1]  # Get tweet ID from URL

            # Take screenshot of the tweet
            screenshot_path = os.path.join(screenshot_dir, f"tweet_{tweet_id}.png")
            tweet_element.screenshot(path=screenshot_path)
            print(f"Screenshot saved: {screenshot_path}")

            # Return tweet details
            return {
                "id": tweet_id,
                "text": tweet_text.strip(),
                "screenshot": screenshot_path
            }
        else:
            print("Tweet not found on the page.")
            return {}


if __name__ == "__main__":
    # Scrape the tweet and capture screenshot
    tweet_url = "https://www.instagram.com/reel/C_GOuAxvXjv/?igsh=bHhqc2IybnVkc3kw"
    tweet_data = scrape_profile(tweet_url)
    
    # Print the tweet content and screenshot path
    print(json.dumps(tweet_data, indent=2))
