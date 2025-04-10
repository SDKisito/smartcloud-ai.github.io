# scripts/seo_audit.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from urllib.parse import urlparse, urljoin
import concurrent.futures
import time

class SEOScanner:
    def __init__(self, base_url):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.internal_links = set()
        self.seo_data = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; SmartCloudAI-SEO-Bot/1.0)'
        }

    def scan_site(self):
        print(f"Starting SEO audit for {self.base_url}")
        start_time = time.time()
        
        self.crawl_site(self.base_url)
        self.analyze_pages()
        
        print(f"Audit completed in {time.time() - start_time:.2f} seconds")
        return pd.DataFrame(self.seo_data)

    def crawl_site(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Add current page to internal links
            self.internal_links.add(url)
            
            # Extract all links
            for link in soup.find_all('a', href=True):
                absolute_url = urljoin(url, link['href'])
                parsed_url = urlparse(absolute_url)
                
                # Keep only internal links from same domain
                if parsed_url.netloc == self.domain and absolute_url not in self.internal_links:
                    self.internal_links.add(absolute_url)
        
        except Exception as e:
            print(f"Error crawling {url}: {str(e)}")

    def analyze_pages(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for url in self.internal_links:
                futures.append(executor.submit(self.analyze_page, url))
            
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    if result:
                        self.seo_data.append(result)
                except Exception as e:
                    print(f"Error in analysis: {str(e)}")

    def analyze_page(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Basic SEO metrics
            title = soup.find('title')
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            canonical = soup.find('link', rel='canonical')
            h1_tags = [h1.text.strip() for h1 in soup.find_all('h1')]
            
            # Image analysis
            images = []
            for img in soup.find_all('img'):
                images.append({
                    'src': img.get('src'),
                    'alt': img.get('alt', ''),
                    'loading': img.get('loading', 'missing')
                })
            
            return {
                'url': url,
                'status_code': response.status_code,
                'title': title.text if title else 'MISSING',
                'title_length': len(title.text) if title else 0,
                'meta_description': meta_desc['content'] if meta_desc else 'MISSING',
                'meta_desc_length': len(meta_desc['content']) if meta_desc else 0,
                'canonical': canonical['href'] if canonical else 'MISSING',
                'h1_count': len(h1_tags),
                'h1_content': h1_tags,
                'image_count': len(images),
                'images_missing_alt': sum(1 for img in images if not img['alt']),
                'lazy_loading': sum(1 for img in images if img['loading'] == 'lazy'),
                'word_count': len(soup.get_text().split()),
                'internal_links_count': len([a for a in soup.find_all('a') 
                                          if urlparse(a.get('href', '')).netloc == self.domain]),
                'external_links_count': len([a for a in soup.find_all('a') 
                                          if urlparse(a.get('href', '')).netloc != self.domain]),
                'response_time': response.elapsed.total_seconds()
            }
            
        except Exception as e:
            print(f"Error analyzing {url}: {str(e)}")
            return None

if __name__ == "__main__":
    scanner = SEOScanner("https://sdkisito.github.io/smartcloud-ai.github.io/")
    results = scanner.scan_site()
    results.to_csv('seo_audit_results.csv', index=False)
    print("Audit results saved to seo_audit_results.csv")