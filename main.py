from database import init_db
from scraper import DocumentationScraper
import argparse

def main():
    # Initialize argument parser
    parser = argparse.ArgumentParser(description='Web Documentation Scraper')
    parser.add_argument('url', help='Base URL of the documentation to scrape')
    args = parser.parse_args()
    
    try:
        # Initialize database
        init_db()
        
        # Create scraper instance
        scraper = DocumentationScraper(args.url)
        
        # Start processing
        print(f"Starting to scrape documentation from: {args.url}")
        scraper.process()
        print("Scraping completed successfully!")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
    finally:
        # Ensure database session is closed
        if 'scraper' in locals():
            scraper.close()

if __name__ == "__main__":
    main()
