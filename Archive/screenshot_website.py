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
    response = requests.get(base_url)
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
    time.sleep(2)  # Allow the page to load

    # Get the total height of the page
    total_height = driver.execute_script("return document.body.scrollHeight")
    viewport_height = driver.execute_script("return window.innerHeight")
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
    output_folder = "screenshots"
    os.makedirs(output_folder, exist_ok=True)

    # Setup Selenium WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    # Get all links on the website
    links = get_all_links(base_url)

    # Take screenshots of all links with scrolling
    for link in links:
        scroll_and_screenshot(driver, output_folder, link)

    driver.quit()
    print("All screenshots have been taken.")

if __name__ == "__main__":
    website_url = input("Enter the website URL: ")
    main(website_url)
