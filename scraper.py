import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from database import Session, Documentation, DocumentationLink
from datetime import datetime

class DocumentationScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.session = Session()
        
    def is_valid_url(self, url):
        """Check if URL belongs to the same domain"""
        return urlparse(url).netloc == self.domain
        
    def get_or_create_documentation(self):
        """Get existing documentation or create new one"""
        doc = self.session.query(Documentation).filter_by(
            base_url=self.base_url
        ).first()
        
        if not doc:
            doc = Documentation(
                base_url=self.base_url,
                domain=self.domain,
                is_processed=False
            )
            self.session.add(doc)
            self.session.commit()
        
        return doc
        
    def extract_links(self, url):
        """Extract all links from a given URL"""
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            links = []
            
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                full_url = urljoin(url, href)
                
                if self.is_valid_url(full_url):
                    links.append({
                        'url': full_url,
                        'title': link.get_text(strip=True)
                    })
            
            return links
            
        except Exception as e:
            print(f"Error extracting links from {url}: {str(e)}")
            return []
            
    def save_links(self, doc_id, links):
        """Save extracted links to database"""
        for link_data in links:
            existing_link = self.session.query(DocumentationLink).filter_by(
                doc_id=doc_id,
                url=link_data['url']
            ).first()
            
            if not existing_link:
                link = DocumentationLink(
                    doc_id=doc_id,
                    url=link_data['url'],
                    title=link_data['title'],
                    is_processed=False
                )
                self.session.add(link)
        
        self.session.commit()
        
    def scrape_content(self, link):
        """Scrape content from a specific link"""
        try:
            response = requests.get(link.url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract main content - customize based on documentation structure
            content = soup.get_text(strip=True)
            
            link.content = content
            link.is_processed = True
            link.last_updated = datetime.utcnow()
            self.session.commit()
            
        except Exception as e:
            print(f"Error scraping content from {link.url}: {str(e)}")
            
    def process(self):
        """Main processing function"""
        # Get or create documentation record
        doc = self.get_or_create_documentation()
        
        if not doc.is_processed:
            # Extract and save all links
            links = self.extract_links(doc.base_url)
            self.save_links(doc.id, links)
            
            # Mark documentation as processed
            doc.is_processed = True
            doc.last_updated = datetime.utcnow()
            self.session.commit()
        
        # Process unprocessed links
        unprocessed_links = self.session.query(DocumentationLink).filter_by(
            doc_id=doc.id,
            is_processed=False
        ).all()
        
        for link in unprocessed_links:
            self.scrape_content(link)
            
    def close(self):
        """Close database session"""
        self.session.close()
