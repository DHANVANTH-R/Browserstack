from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from collections import Counter
import requests
import os
import time
import re
from googletrans import Translator
import logging
from selenium.webdriver.chrome.options import Options as ChromeOptions
options = ChromeOptions()
#options.set_capability('sessionName', 'BStack Sample Test')
driver = webdriver.Chrome(options=options)
driver.maximize_window()


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the translator
translator = Translator()

# Global list to store translated headers
translated_headers = []




def download_image(image_url, file_name):
    """Downloads an image from the given URL and saves it with the specified file name."""
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        image_path = os.path.join(os.getcwd(), file_name)
        with open(image_path, 'wb') as file:
            file.write(response.content)
        logging.info(f"Image saved as {file_name}")
    except Exception as e:
        logging.error(f"Failed to download image: {e}")

def extract_article_data(driver, article_index):
    """Extracts data from an article specified by its index."""
    try:
        logging.info(f"Extracting data for article {article_index}...")
        article_xpath = f'/html/body/main/div[2]/section[1]/div/div/article[{article_index}]/header/h2/a'
        article_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, article_xpath))
        )
        article_link.click()

        # Extract title
        title_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/article/header/div[1]/h1'))
        )
        title_text = title_element.text

        # Translate title to English
        translated_title = translator.translate(title_text, src='es', dest='en').text
        translated_headers.append(translated_title)  # Store the translated header

        # Extract content
        content_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/article/header/div[1]/h2'))
        )
        content_text = content_element.text

        # Extract image URL
        image_element = driver.find_element(By.XPATH, '/html/body/article/header/div[2]/figure/span/img')
        image_url = image_element.get_attribute("src")

        logging.info(f"Article {article_index} - Title: {title_text}")
        logging.info(f"Article {article_index} - Translated Title: {translated_title}")
        logging.info(f"Article {article_index} - Content: {content_text}")
        logging.info(f"Article {article_index} - Image URL: {image_url}")

        # Download the image
        download_image(image_url, f"Article{article_index}.jpg")

    except TimeoutException as e:
        logging.error(f"Timeout while extracting article {article_index}: {e}")
    except Exception as e:
        logging.error(f"Error extracting article {article_index}: {e}")
    finally:
        # Navigate back to the main page
        driver.get("https://elpais.com/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "main")))

def analyze_headers():
    """Analyzes the translated headers for repeated words."""
    # Combine all headers into a single string
    combined_text = " ".join(translated_headers).lower()

    # Tokenize and count word occurrences
    words = re.findall(r'\b\w+\b', combined_text)
    word_counts = Counter(words)

    # Filter words that are repeated more than twice
    repeated_words = {word: count for word, count in word_counts.items() if count > 2}

    for word, count in repeated_words.items():
        print(f"{word}: {count}")

# Main script
def main():
    """Main function to scrape, translate, and analyze articles."""
    
    try:
        # Open the website
        url = "https://elpais.com/"
        logging.info("Opening website...")
        driver.get(url)
        time.sleep(10)
        # Accept cookies
        logging.info("Accepting cookies...")
        try:
            time.sleep(10)
            accept_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'didomi-notice-agree-button'))
            )
            accept_button.click()
            logging.info("Cookies accepted.")

        except TimeoutException:
            logging.warning("Cookies accept button not found. Continuing with the next step.")
        except Exception as e:
            logging.error(f"An error occurred while handling the cookies accept button: {e}")

        # Extract data from the first 5 articles
        for i in range(1, 6):
            extract_article_data(driver, i)

        # Analyze the translated headers
        print("\nWords that are repeated more than twice across all headers combined")
        analyze_headers()

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()