import requests
from bs4 import BeautifulSoup
import logging
from typing import List, Dict
import re
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

class WebScraper:
    def __init__(self, base_url: str = "https://www.veritus.ai/"):
        self.base_url = base_url
        self.visited_urls = set()
        self.documents = []

    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        return text.strip()

    def extract_text_from_url(self, url: str) -> List[Dict]:
        """Extract text content from a URL"""
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            text = self.clean_text(text)
            
            # Split into chunks (approximately 500 characters)
            chunks = []
            current_chunk = ""
            words = text.split()
            
            for word in words:
                if len(current_chunk) + len(word) + 1 <= 500:
                    current_chunk += " " + word
                else:
                    if current_chunk:
                        chunks.append({
                            "text": current_chunk.strip(),
                            "source": url
                        })
                    current_chunk = word
            
            if current_chunk:
                chunks.append({
                    "text": current_chunk.strip(),
                    "source": url
                })
            
            return chunks
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return []

    def crawl_website(self, max_pages: int = 10) -> List[Dict]:
        """Crawl the website and extract text content"""
        urls_to_visit = {self.base_url}
        self.visited_urls = set()
        self.documents = []
        
        while urls_to_visit and len(self.visited_urls) < max_pages:
            url = urls_to_visit.pop()
            
            if url in self.visited_urls:
                continue
                
            self.visited_urls.add(url)
            logger.info(f"Scraping: {url}")
            
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract text content
                chunks = self.extract_text_from_url(url)
                self.documents.extend(chunks)
                
                # Find new URLs to visit
                for link in soup.find_all('a', href=True):
                    new_url = urljoin(url, link['href'])
                    if new_url.startswith(self.base_url) and new_url not in self.visited_urls:
                        urls_to_visit.add(new_url)
                        
            except Exception as e:
                logger.error(f"Error processing {url}: {str(e)}")
        
        return self.documents 