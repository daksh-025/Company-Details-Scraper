import utils.session
import re
from serpapi.google_search import GoogleSearch

# SerpAPI API Key (Replace with your actual key)
SERPAPI_KEY = "69db8921e26eadf7a230ab12cd1fc3aec8b0c84573450e1aee573b93809d8070"

# Function to fetch website
def fetch_website(company_number, company_name):
    search_query = f"{company_number} {company_name} UK company official site"
    
    search_params = {
        "q": search_query,
        "location": "United Kingdom",
        "api_key": SERPAPI_KEY,
        "num": 3  # Fetch multiple, return the first valid one
    }
    
    search = GoogleSearch(search_params)
    results = search.get_dict()
    
    for result in results.get("organic_results", []):
        link = result.get("link", "")
        if "linkedin.com" not in link:  # Ensure it's not LinkedIn
            return link  # Return the first valid website link

    return "Website not found"

# Function to fetch LinkedIn profile
def fetch_linkedin(company_number, company_name):
    search_query = f"{company_number} {company_name} LinkedIn profile"
    
    search_params = {
        "q": search_query,
        "location": "United Kingdom",
        "api_key": SERPAPI_KEY,
        "num": 3
    }
    
    search = GoogleSearch(search_params)
    results = search.get_dict()
    
    for result in results.get("organic_results", []):
        link = result.get("link", "")
        if "linkedin.com/company" in link:  # Ensure it's a company profile
            return link

    return "LinkedIn profile not found"

# Get user input
company_number = input("Enter Company Number: ").strip()
company_name = input("Enter Company Name: ").strip()

# Fetch details
website = fetch_website(company_number, company_name)
linkedin = fetch_linkedin(company_number, company_name)

# Display results
print("\n--- Company Details ---")
print(f"Company Number: {company_number}")
print(f"Company Name: {company_name}")
print(f"Website: {website}")
print(f"LinkedIn Profile: {linkedin}")