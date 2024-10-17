import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

def get_all_links(base_url):
    """Fetch all unique subpage links from the base URL."""
    response = requests.get(base_url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = set()

    for a_tag in soup.find_all('a', href=True):
        link = urljoin(base_url, a_tag['href'])
        if urlparse(link).netloc == urlparse(base_url).netloc:  # Same domain
            links.add(link)

    return links

def scroll_and_screenshot(driver, output_folder, url):
    """Scrolls down the page, taking screenshots of each section."""
    driver.get(url)
    time.sleep(5)  # Allow the page to load

    # Get the total height of the page
    total_height = driver.execute_script("return document.body.scrollHeight")
    viewport_height = 1080  # Set viewport height to 1080 pixels (full HD)
    scroll_amount = viewport_height  # Amount to scroll each time
    scroll_position = 0
    screenshot_count = 1

    # Prepare file naming
    file_name_base = urlparse(url).path.strip('/').replace('/', '_') or 'home'
    
    # Scroll and take screenshots
    while scroll_position < total_height:
        # Save screenshot of the current view
        screenshot_path = os.path.join(output_folder, f"{file_name_base}_part_{screenshot_count}.png")
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved: {screenshot_path}")

        # Scroll down
        scroll_position += scroll_amount
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")
        time.sleep(1)  # Pause to allow animations and loading
        screenshot_count += 1

def main(base_url):
    # Create an output directory
    output_folder = "screenshots-2"
    os.makedirs(output_folder, exist_ok=True)

    # Setup Selenium WebDriver with a viewport of 1920x1080
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")  # Set default window size to 1920x1080
    chrome_options.add_argument("--ignore-certificate-errors")  # Ignore SSL certificate errors
    chrome_options.add_argument("--allow-insecure-localhost")  # If testing with localhost


    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    # Get all links on the website
    links = get_all_links(base_url)
    total_links = len(links)  # Count total links

    # Take screenshots of all links with scrolling
    for index, link in enumerate(links):
        scroll_and_screenshot(driver, output_folder, link)

        # Calculate and print the loading status
        percentage_complete = (index + 1) / total_links * 100
        print(f"Progress: {percentage_complete:.2f}% - Processed: {index + 1}/{total_links} links")

    driver.quit()
    print("All screenshots have been taken.")

if __name__ == "__main__":
    website_url = input("Enter the website URL: ")
    main(website_url)
