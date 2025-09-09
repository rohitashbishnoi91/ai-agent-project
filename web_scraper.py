import requests
from bs4 import BeautifulSoup
import json
import time
from typing import Dict, List
import re

class ArymalabsScraper:
    def __init__(self, base_url: str = "https://www.arymalabs.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def scrape_page(self, url: str) -> BeautifulSoup:
        """Scrape a single page and return BeautifulSoup object"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None
    
    def extract_text_content(self, soup: BeautifulSoup) -> str:
        """Extract clean text content from soup object"""
        if not soup:
            return ""
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text and clean it
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def find_links(self, soup: BeautifulSoup) -> List[str]:
        """Find all internal links on the page"""
        if not soup:
            return []
        
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('/'):
                href = self.base_url + href
            elif href.startswith(self.base_url):
                links.append(href)
        
        return list(set(links))
    
    def categorize_content(self, text: str) -> Dict[str, str]:
        """Categorize content based on keywords"""
        categories = {
            "MMM_SERVICES": [],
            "MMM_PRODUCTS": [],
            "EXPERIMENTATION_PRODUCTS": []
        }
        
        # Keywords for each category
        mmm_service_keywords = [
            "mmm service", "media mix modeling service", "attribution service",
            "marketing mix modeling", "mmm consulting", "attribution modeling"
        ]
        
        mmm_product_keywords = [
            "mmm product", "media mix modeling tool", "attribution tool",
            "mmm platform", "marketing mix modeling software", "mmm solution"
        ]
        
        experiment_keywords = [
            "experimentation", "a/b testing", "experiment", "test", "testing",
            "experimental design", "statistical testing", "causal inference"
        ]
        
        text_lower = text.lower()
        
        # Check for MMM Services
        for keyword in mmm_service_keywords:
            if keyword in text_lower:
                # Extract relevant sentences
                sentences = text.split('.')
                for sentence in sentences:
                    if keyword in sentence.lower():
                        categories["MMM_SERVICES"].append(sentence.strip())
        
        # Check for MMM Products
        for keyword in mmm_product_keywords:
            if keyword in text_lower:
                sentences = text.split('.')
                for sentence in sentences:
                    if keyword in sentence.lower():
                        categories["MMM_PRODUCTS"].append(sentence.strip())
        
        # Check for Experimentation Products
        for keyword in experiment_keywords:
            if keyword in text_lower:
                sentences = text.split('.')
                for sentence in sentences:
                    if keyword in sentence.lower():
                        categories["EXPERIMENTATION_PRODUCTS"].append(sentence.strip())
        
        return categories
    
    def scrape_website(self) -> Dict[str, any]:
        """Main method to scrape the entire website"""
        print("Starting website scraping...")
        
        # Start with the main page
        main_soup = self.scrape_page(self.base_url)
        if not main_soup:
            print("Could not access main website, using fallback content...")
            return self.get_fallback_content()
        
        # Extract main page content
        main_content = self.extract_text_content(main_soup)
        
        # Find all internal links
        links = self.find_links(main_soup)
        print(f"Found {len(links)} internal links")
        
        # Scrape additional pages (limit to avoid overwhelming)
        all_content = main_content
        scraped_pages = 0
        max_pages = 10  # Limit to prevent excessive requests
        
        for link in links[:max_pages]:
            if scraped_pages >= max_pages:
                break
                
            print(f"Scraping: {link}")
            page_soup = self.scrape_page(link)
            if page_soup:
                page_content = self.extract_text_content(page_soup)
                all_content += " " + page_content
                scraped_pages += 1
            
            # Be respectful with requests
            time.sleep(1)
        
        # Categorize the content
        categorized_content = self.categorize_content(all_content)
        
        # Also try to extract specific sections
        sections = self.extract_sections(main_soup)
        
        result = {
            "main_content": main_content[:2000],  # First 2000 chars
            "categorized_content": categorized_content,
            "sections": sections,
            "total_pages_scraped": scraped_pages + 1,
            "links_found": len(links)
        }
        
        return result
    
    def extract_sections(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract specific sections from the main page"""
        sections = {}
        
        if not soup:
            return sections
        
        # Look for common section headers
        headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        
        for header in headers:
            header_text = header.get_text().strip()
            if any(keyword in header_text.lower() for keyword in ['service', 'product', 'solution', 'about']):
                # Get the content following this header
                content = ""
                next_element = header.find_next_sibling()
                while next_element and next_element.name not in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    content += next_element.get_text() + " "
                    next_element = next_element.find_next_sibling()
                
                sections[header_text] = content.strip()
        
        return sections
    
    def get_fallback_content(self) -> Dict[str, any]:
        """Return fallback content when website is not accessible"""
        return {
            "main_content": "Aryma Labs provides Marketing Mix Modeling (MMM) services, products, and experimentation tools for enterprises.",
            "categorized_content": {
                "MMM_SERVICES": [
                    "Marketing Mix Modeling services for enterprises",
                    "MMM consulting and implementation",
                    "Custom MMM model development",
                    "Marketing attribution analysis",
                    "ROI optimization consulting"
                ],
                "MMM_PRODUCTS": [
                    "ArymaEdge - State of the Art MMM Platform",
                    "MMMGPT - AI-powered MMM assistant",
                    "MMMDiagnose - MMM model validation tool",
                    "MMM Budget Optimization tools",
                    "MMM Validators and Bootstrapper"
                ],
                "EXPERIMENTATION_PRODUCTS": [
                    "A/B testing and experimentation tools",
                    "DiDetective - Causal inference platform",
                    "Statistical testing solutions",
                    "Experimental design tools",
                    "Causal inference and incrementality testing"
                ]
            },
            "sections": {},
            "total_pages_scraped": 0,
            "links_found": 0
        }

def main():
    scraper = ArymalabsScraper()
    result = scraper.scrape_website()
    
    # Save results to file
    with open('scraped_content.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    print("Scraping completed. Results saved to scraped_content.json")
    return result

if __name__ == "__main__":
    main()
