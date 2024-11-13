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
        screenshot_desktop.main_desktop(website_url)
        screenshot_iphone12pro.main_iphone(website_url)
    else:
        print("Invalid choice. Please run the script again and select 1, 2, or 3.")

if __name__ == "__main__":
    main()
