import threading
from scripts import screenshot_desktop, screenshot_iphone12pro

def main():
    # Get URL from the user
    website_url = input("Enter the website URL: ")

    # Get device choice from the user
    print("Choose the version to run:")
    print("1: Desktop")
    print("2: iPhone")
    print("3: Both")
    choice = input("Enter your choice (1, 2, or 3): ")

    # Execute based on user choice
    if choice == '1':
        screenshot_desktop.main_desktop(website_url)
    elif choice == '2':
        screenshot_iphone12pro.main_iphone(website_url)
    elif choice == '3':
        desktop_thread = threading.Thread(target=screenshot_desktop.main_desktop, args=(website_url,))
        iphone_thread = threading.Thread(target=screenshot_iphone12pro.main_iphone, args=(website_url,))

        # Start the threads
        desktop_thread.start()
        iphone_thread.start()
        
        # Wait for both threads to finish
        desktop_thread.join()
        iphone_thread.join()
    else:
        print("Invalid choice. Please run the script again and select 1, 2, or 3.")

if __name__ == "__main__":
    main()
