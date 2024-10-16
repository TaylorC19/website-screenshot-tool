import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

def get_all_links(base_url, visited=None):
    """Recursively fetch all unique subpage links from the base URL."""
    if visited is None:
        visited = set()

    # Avoid re-visiting the same page
    if base_url in visited:
        return visited

    visited.add(base_url)

    # Fetch and parse the base page
    response = requests.get(base_url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = set()

    # Find all unique internal links
    for a_tag in soup.find_all('a', href=True):
        link = urljoin(base_url, a_tag['href'])
        if urlparse(link).netloc == urlparse(base_url).netloc:  # Same domain
            links.add(link)

    # Visit each new link recursively
    for link in links:
        if link not in visited:
            get_all_links(link, visited)

    return visited

def scroll_and_screenshot(driver, output_folder, url):
    """Scrolls down the page, taking screenshots of each section."""
    driver.get(url)
    time.sleep(2)  # Allow the page to load

    # Get the total height of the page
    total_height = driver.execute_script("return document.body.scrollHeight")
    viewport_height = 1080  # Set viewport height to 1080 pixels (1080p)
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
    output_folder = "screenshots-1080p-withrecursion"
    os.makedirs(output_folder, exist_ok=True)

    # Setup Chrome options for 1080p resolution
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--window-size=1920,1080")  # Set window size to 1920x1080
    chrome_options.add_argument("--ignore-certificate-errors")  # Ignore SSL certificate errors
    chrome_options.add_argument("--allow-insecure-localhost")  # If testing with localhost

    # chrome_options.add_argument("--headless")  # Uncomment if you want to run in headless mode

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
    website_url = input("Enter the website URL (starting with http:// or https://): ")
    main(website_url)
