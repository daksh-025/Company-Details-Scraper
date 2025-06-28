from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Function to perform a Google Search using Selenium
def google_search(query):
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (no UI)
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Setup WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Open Google Search
        driver.get(f"https://www.google.com/search?q={query.replace(' ', '+')}")
        
        # Wait until search results are loaded
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'h3')))

        # Scroll the page to load more results (Google lazy loads more results as you scroll)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Allow time for more results to load

        # Find all search result links by searching for anchor (<a>) tags
        search_results = driver.find_elements(By.CSS_SELECTOR, 'a')

        links = []
        for result in search_results:
            href = result.get_attribute("href")
            if href and "http" in href:  # Ensure it's a valid URL
                links.append(href)

        # Return the first link
        if links:
            return links[0]  # Return the first relevant link
    except Exception as e:
        print("Error:", e)
    finally:
        driver.quit()  # Close the browser

    return "Not Found"

# Example Usage
company_name = "Tesco PLC"
company_number = "00445790"

website_query = f"{company_number} {company_name} UK company official site"
linkedin_query = f"{company_number} {company_name} LinkedIn profile"

website = google_search(website_query)
linkedin = google_search(linkedin_query)

print("Website:", website)
print("LinkedIn:", linkedin)
