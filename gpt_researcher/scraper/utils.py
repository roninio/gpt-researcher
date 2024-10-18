from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging

def get_relevant_images(soup: BeautifulSoup, url: str) -> list:
    """Extract relevant images from the page"""
    image_urls = []
    
    try:
        # Find all img tags with src attribute
        all_images = soup.find_all('img', src=True)
        
        for img in all_images:
            img_src = urljoin(url, img['src'])
            if img_src.startswith(('http://', 'https://')):
                # Check for relevant classes
                if any(cls in img.get('class', []) for cls in ['header', 'featured', 'hero', 'thumbnail', 'main', 'content']):
                    image_urls.append((img_src, 3))  # Higher priority
                # Check for size attributes
                elif img.get('width') and img.get('height'):
                    width = int(img['width'])
                    height = int(img['height'])
                    if width >= 1200 and height >= 600:
                        image_urls.append((img_src, 2))  # Medium priority
                    elif width >= 800 or height >= 400:
                        image_urls.append((img_src, 1))  # Lower priority
        
        # Sort images by priority (highest first) and then limit to top 10
        sorted_images = sorted(image_urls, key=lambda x: x[1], reverse=True)
        return [img[0] for img in sorted_images[:10]]
    
    except Exception as e:
        logging.error(f"Error in get_relevant_images: {e}")
        return []