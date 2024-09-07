from playwright.sync_api import sync_playwright


def scrape_profile(url: str) -> dict:
    """
    Scrape an X.com profile details, e.g.: https://x.com/Scrapfly_dev
    """
    _xhr_calls = []

    def intercept_response(response):
        """Capture all background requests and save them"""
        # we can extract details from background requests
        if response.request.resource_type == "xhr":
            _xhr_calls.append(response)
        return response

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)  # Launches browser in non-headless mode
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        # Enable background request intercepting:
        page.on("response", intercept_response)
        
        # Go to URL and wait for the page to load
        page.goto(url)
        page.wait_for_selector("[data-testid='primaryColumn']")

        # Find all tweet background requests:
        tweet_calls = [f for f in _xhr_calls if "UserBy" in f.url]
        for xhr in tweet_calls:
            data = xhr.json()
            return data['data']['user']['result']

    return {}


if __name__ == "__main__":
    # Run synchronously since sync_playwright is used
    print(scrape_profile("https://x.com/elonmusk?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor"))



# from playwright.sync_api import sync_playwright
# import json


# def scrape_profile(url: str) -> dict:
#     """
#     Scrape an X.com profile details and fetch recent posts and comments.
#     """
#     _xhr_calls = []

#     def intercept_response(response):
#         """Capture all background requests and save them"""
#         if response.request.resource_type == "xhr":
#             _xhr_calls.append(response)

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
#         for _ in range(5):  # Adjust the range to load more tweets if needed
#             page.mouse.wheel(0, 3000)  # Scroll down by 3000 pixels
#             page.wait_for_timeout(2000)  # Wait for the new tweets to load

#         # Find all XHR requests that contain user and tweet data:
#         tweet_calls = [f for f in _xhr_calls if "TweetDetail" in f.url or "TweetById" in f.url]
#         reply_calls = [f for f in _xhr_calls if "TweetResult" in f.url and "conversation" in f.url]

#         # Extract tweet data:
#         tweets = []
#         for tweet_call in tweet_calls:
#             try:
#                 tweet_data = tweet_call.json()
#                 tweet_legacy = tweet_data['data']['tweet']['legacy']
#                 tweets.append({
#                     "id": tweet_data['data']['tweet']['rest_id'],
#                     "text": tweet_legacy.get('full_text', ''),
#                     "favorites": tweet_legacy.get('favorite_count', 0),
#                     "retweets": tweet_legacy.get('retweet_count', 0),
#                     "comments": []  # Will be filled with comments later
#                 })
#             except Exception as e:
#                 print(f"Error processing tweet data: {e}")

#         # Extract replies/comments:
#         for reply_call in reply_calls:
#             try:
#                 reply_data = reply_call.json()
#                 conversation_thread = reply_data['data']['threaded_conversation_with_injections']['instructions'][0]['entries']
                
#                 tweet_id = conversation_thread[0]['content']['itemContent']['tweet_results']['result']['rest_id']
                
#                 # Extract all comments/replies to this tweet
#                 comments = []
#                 for entry in conversation_thread:
#                     if "tweet_results" in entry['content']['itemContent']:
#                         comment_text = entry['content']['itemContent']['tweet_results']['result']['legacy'].get('full_text', '')
#                         comments.append(comment_text)

#                 # Match the replies to the corresponding tweet
#                 for tweet in tweets:
#                     if tweet['id'] == tweet_id:
#                         tweet['comments'] = comments
#             except Exception as e:
#                 print(f"Error processing reply data: {e}")

#         return {
#             "tweets": tweets
#         }


# if __name__ == "__main__":
#     # Scrape the profile and print the result
#     profile_url = "https://x.com/elonmusk?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor"
#     profile_data = scrape_profile(profile_url)
#     print(json.dumps(profile_data, indent=2))
