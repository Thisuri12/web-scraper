import httpx
from bs4 import BeautifulSoup
import re
import pandas as pd
from urllib.parse import urljoin, urlparse
from utils import is_valid_email
import os
from dotenv import load_dotenv

EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
PHONE_REGEX = r"(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{2,4}\)?[\s.-]?)?\d{3,4}[\s.-]?\d{3,4}"
BRAVE_API_KEY = BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")

def search_company_website(company, region, country):
    query = f"{company} {region} {country} contact email"
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": BRAVE_API_KEY
    }
    params = {
        "q": query,
        "count": 1
    }
    try:
        response = httpx.get("https://api.search.brave.com/res/v1/web/search", headers=headers, params=params, timeout=10)
        data = response.json()
        url = data["web"]["results"][0]["url"]
        print(f"Brave URL for {company}: {url}")
        if any(domain in url for domain in ["linkedin.com", "facebook.com", "twitter.com", "yelp.com"]):
            return None
        return url
    except Exception as e:
        print(f"Brave API error for {company}: {e}")
        return None

def find_contact_page(base_url, soup):
    contact_keywords = [
        "contact", "about", "support", "help",
        "contatti", "chi-siamo", "assistenza", "supporto"
    ]
    links = soup.find_all("a", href=True)
    for link in links:
        href = link["href"].lower()
        if any(keyword in href for keyword in contact_keywords):
            full_url = urljoin(base_url, href)
            if urlparse(full_url).netloc == urlparse(base_url).netloc:
                return full_url
    return base_url

def scrape_emails(df, country, progress_callback=None):
    results = []
    total = len(df)

    for i, row in enumerate(df.itertuples(index=False), start=1):
        company = row.Company
        region = row.Region
        url = search_company_website(company, region, country)

        email_result = "N/A"
        phone_result = "N/A"

        if not url or not url.startswith("http"):
            results.append({
                "Company": company,
                "Region": region,
                "Website": "Invalid or unsupported URL",
                "Emails": email_result,
                "Phone Numbers": phone_result
            })
            if progress_callback:
                progress_callback(i, total, company)
            continue

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        timeout_config = httpx.Timeout(connect=10.0, read=30.0, write=10.0, pool=5.0)

        try:
            response = httpx.get(url, headers=headers, timeout=timeout_config, verify=True, follow_redirects=True)
            soup = BeautifulSoup(response.text, "lxml")
            contact_url = find_contact_page(url, soup)
        except Exception as e:
            print(f"Error loading homepage for {company}: {e}")
            contact_url = url  # fallback to homepage

        try:
            contact_response = httpx.get(contact_url, headers=headers, timeout=30, verify=True, follow_redirects=True)
            contact_soup = BeautifulSoup(contact_response.text, "lxml")

            try:
                emails = re.findall(EMAIL_REGEX, contact_soup.text)
                filtered_emails = [e for e in emails if is_valid_email(e)]
                email_result = filtered_emails[0] if filtered_emails else "No valid email found"
            except Exception as e:
                print(f"Email extraction failed for {company}: {e}")
                email_result = "Error fetching"

            try:
                phones = re.findall(PHONE_REGEX, contact_soup.text)
                cleaned_phones = [p.strip().replace("+", "") for p in phones]
                filtered_phones = [p for p in cleaned_phones if 9 <= len(p) <= 12]
                phone_result = filtered_phones[0] if filtered_phones else "No phone number found"
            except Exception as e:
                print(f"Phone extraction failed for {company}: {e}")
                phone_result = "Error fetching"

        except Exception as e:
            print(f"Error loading contact page for {company}: {e}")
            email_result = "Error fetching"
            phone_result = "Error fetching"

        results.append({
            "Company": company,
            "Region": region,
            "Website": url,
            "Emails": email_result,
            "Phone Numbers": phone_result
        })

        if progress_callback:
            progress_callback(i, total, company)

    return pd.DataFrame(results)
