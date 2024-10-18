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

def wait_for_network_idle(driver, timeout=10):
    """Wait until there are no more network requests."""
    start_time = time.time()

    while time.time() - start_time < timeout:
        # Use a try-catch to handle potential JavaScript exceptions
        try:
            # Fetch Chrome's performance logs, filtering out problematic entries
            logs = driver.execute_script("""
                const entries = window.performance.getEntries();
                return entries.map(entry => ({
                    name: entry.name,
                    entryType: entry.entryType,
                    startTime: entry.startTime,
                    duration: entry.duration,
                    responseEnd: entry.responseEnd || 0
                }));
            """)
        except Exception as e:
            print(f"Error fetching performance entries: {e}")
            return False

        # Filter for network requests
        network_logs = [log for log in logs if log['entryType'] in ['resource', 'navigation']]

        # Check if there are any unfinished requests
        unfinished_requests = [log for log in network_logs if log['responseEnd'] == 0]

        # If there are no unfinished requests, we're done
        if not unfinished_requests:
            return True

        time.sleep(1)  # Pause briefly before checking again

    print("Warning: Network activity didn't fully settle within the timeout.")
    return False

def wait_for_images_to_load(driver):
    """Wait for all images in the current viewport to be fully loaded, including lazy-loaded images."""
    timeout = 10  # Set a timeout to avoid infinite waiting
    start_time = time.time()

    while time.time() - start_time < timeout:
        # Check if all images in the viewport are loaded
        all_images_loaded = driver.execute_script("""
            const images = Array.from(document.images);
            const lazyImages = images.filter(img => {
                const rect = img.getBoundingClientRect();
                return rect.top < window.innerHeight && rect.bottom >= 0; // Images in the viewport
            });
            return lazyImages.every(img => img.complete && img.naturalHeight > 0);
        """)

        if all_images_loaded:
            return True  # All images loaded

        time.sleep(1)  # Wait a little before re-checking

    print("Warning: Not all images fully loaded within the timeout.")
    return False

def scroll_and_screenshot(driver, output_folder, url):
    """Scrolls down the page, waiting for images to load, and taking screenshots of each section."""
    driver.get(url)
    time.sleep(5)  # Allow more time for the page to load

    # Wait for initial images to load
    if not wait_for_images_to_load(driver):
        print(f"Warning: Initial images did not fully load on {url}")

    # Get the total height of the page
    total_height = driver.execute_script("return document.body.scrollHeight")
    viewport_height = 844  # Set viewport height to 844 pixels (iPhone 12 Pro)
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

        # Wait for lazy-loaded images to appear after scrolling
        if not wait_for_images_to_load(driver):
            print(f"Warning: Lazy-loaded images did not fully load after scrolling on {url}")

        # Allow a brief pause for any animations or other loading
        time.sleep(1.5)
        screenshot_count += 1

def main(base_url):
    # Create an output directory
    output_folder = "screenshots-iphone12pro"
    os.makedirs(output_folder, exist_ok=True)

    # Setup mobile emulation for iPhone 12 Pro
    mobile_emulation = {
        "deviceMetrics": { "width": 390, "height": 844, "pixelRatio": 3.0 },
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
    }

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    chrome_options.add_argument("--ignore-certificate-errors")  # Ignore SSL certificate errors
    chrome_options.add_argument("--allow-insecure-localhost")  # If testing with localhost
    
    # Enable performance logging
    chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

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
