# scripts/sitemap_generator.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import xml.etree.ElementTree as ET
from datetime import datetime

def get_all_urls(base_url):
    """Récupère toutes les URLs internes du site"""
    domain = urlparse(base_url).netloc
    visited = set()
    to_visit = {base_url}
    headers = {'User-Agent': 'SmartCloudAI-Sitemap-Generator/1.0'}

    while to_visit:
        url = to_visit.pop()
        try:
            print(f"Scanning: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            visited.add(url)
            
            for link in soup.find_all('a', href=True):
                absolute_url = urljoin(url, link['href'])
                parsed = urlparse(absolute_url)
                
                if (parsed.netloc == domain 
                    and not parsed.fragment
                    and absolute_url not in visited
                    and absolute_url not in to_visit):
                    to_visit.add(absolute_url)
                    
        except Exception as e:
            print(f"Error scanning {url}: {str(e)}")
    
    return sorted(visited)

def generate_sitemap(urls, output_file="sitemap.xml"):
    """Génère un fichier sitemap.xml"""
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    for url in urls:
        url_element = ET.SubElement(urlset, "url")
        ET.SubElement(url_element, "loc").text = url
        ET.SubElement(url_element, "lastmod").text = datetime.now().strftime("%Y-%m-%d")
        priority = "1.0" if url == urls[0] else "0.8"
        ET.SubElement(url_element, "priority").text = priority
    
    tree = ET.ElementTree(urlset)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)
    print(f"Sitemap généré avec {len(urls)} URLs dans {output_file}")

if __name__ == "__main__":
    site_url = "https://sdkisito.github.io/smartcloud-ai.github.io/"
    urls = get_all_urls(site_url)
    generate_sitemap(urls)