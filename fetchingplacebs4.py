import requests
from bs4 import BeautifulSoup
import random
import time

# Function to scrape Google search results
def google_scrape(query):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    #print(soup)
    found_links = []
    
    for link in soup.find_all("a"):
        href = link.get("href")
        print(href)
        if href and href.startswith("/url?q="):  # Ensure href is valid
            clean_url = href.split("/url?q=")[1].split("&")[0]  # Extract clean URL
            if not keyword_filters or any(kw in clean_url for kw in keyword_filters):
                found_links.append(clean_url)  # Store matching links
    
    return found_links if found_links else ["Not Found"]



# Example Usage
time.sleep(random.uniform(1, 3))  # Avoid bot detection
website = google_scrape("Tesco PLC UK official site")
linkedin = google_scrape("Tesco PLC LinkedIn profile")

print("Website:", website)
print("LinkedIn:", linkedin)
