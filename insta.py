from playwright.sync_api import sync_playwright
import os
from textblob import TextBlob  # NLP library for sentiment analysis
from PIL import Image
import pytesseract

def take_screenshot_and_extract_text(url: str):
    """
    Scrape an Instagram post, take a screenshot, extract comments, and apply NLP.
    Save the screenshot and comments in separate files.
    """
    screenshot_dir = "instagram_screenshots"
    comments_dir = "instagram_comments"

    # Create directories if they don't exist
    os.makedirs(screenshot_dir, exist_ok=True)
    os.makedirs(comments_dir, exist_ok=True)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)  # Launch browser in non-headless mode
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        # Go to the Instagram post URL
        page.goto(url)

        try:
            # Wait for the post to load
            page.wait_for_selector("article", timeout=10000)

            # Extract post ID from URL
            post_id = url.split('/')[-2]

            # Step 1: Capture screenshot of the post
            screenshot_path = os.path.join(screenshot_dir, f"post_{post_id}.png")
            page.screenshot(path=screenshot_path)
            print(f"Screenshot saved: {screenshot_path}")

            # Step 2: Extract text from the screenshot using OCR
            extracted_text = extract_text_from_image(screenshot_path)
            if extracted_text:
                # Save extracted text into a file
                text_file_path = os.path.join(comments_dir, f"extracted_text_{post_id}.txt")
                with open(text_file_path, "w", encoding="utf-8") as text_file:
                    text_file.write(extracted_text)
                print(f"Extracted text saved: {text_file_path}")

                # Step 3: Apply NLP to the extracted text (Sentiment Analysis using TextBlob)
                analyze_text(extracted_text)
            else:
                print("No text found in the screenshot!")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            browser.close()

def extract_text_from_image(image_path: str) -> str:
    """
    Extract text from an image using OCR.
    """
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return ""

def analyze_text(text: str):
    """
    Analyze the text using basic sentiment analysis and display the results.
    """
    print("\nAnalyzing text...")

    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity  # Sentiment polarity: -1 (negative) to 1 (positive)
    print(f"Extracted Text: {text}")
    print(f"Sentiment Score: {sentiment}\n")
    
    print("Analysis complete.")

if __name__ == "__main__":
    # Provide an Instagram post URL to scrape, screenshot, and analyze comments
    post_url = "https://www.instagram.com/p/C82UlomxBy9/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA=="  # Replace with any Instagram post URL
    take_screenshot_and_extract_text(post_url)
