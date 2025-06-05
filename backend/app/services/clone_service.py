import os
from typing import Optional
import requests
from bs4 import BeautifulSoup
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class CloneService:
    def __init__(self):
        self.anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
    async def scrape_website(self, url: str) -> Optional[str]:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract useful design context
            styles = []
            for style in soup.find_all('style'):
                styles.append(style.string)
            
            # Get inline styles
            inline_styles = []
            for tag in soup.find_all(attrs={'style': True}):
                inline_styles.append(f"{tag.name}: {tag['style']}")
            
            # Get background colors
            background_colors = []
            # Check body background
            body = soup.find('body')
            if body and body.get('style'):
                if 'background' in body['style'] or 'background-color' in body['style']:
                    background_colors.append(f"body: {body['style']}")
            
            # Check html background
            html = soup.find('html')
            if html and html.get('style'):
                if 'background' in html['style'] or 'background-color' in html['style']:
                    background_colors.append(f"html: {html['style']}")
            
            # Extract header content and styles
            header_content = []
            header = soup.find(['header', 'nav', 'div'], class_=lambda x: x and ('header' in x.lower() or 'nav' in x.lower()))
            if header:
                header_content.append({
                    'html': str(header),
                    'styles': header.get('style', ''),
                    'classes': header.get('class', [])
                })
            
            # Extract footer content and styles
            footer_content = []
            footer = soup.find(['footer', 'div'], class_=lambda x: x and 'footer' in x.lower())
            if footer:
                footer_content.append({
                    'html': str(footer),
                    'styles': footer.get('style', ''),
                    'classes': footer.get('class', [])
                })
            
            # Get images
            images = []
            for img in soup.find_all('img'):
                if img.get('src'):
                    images.append({
                        'src': img['src'],
                        'alt': img.get('alt', ''),
                        'style': img.get('style', '')
                    })
            
            # Get all CSS classes and their styles
            class_styles = {}
            for tag in soup.find_all(class_=True):
                for class_name in tag.get('class', []):
                    if class_name not in class_styles:
                        class_styles[class_name] = tag.get('style', '')
            
            # Combine all context
            context = {
                'html': response.text,
                'styles': styles,
                'inline_styles': inline_styles,
                'background_colors': background_colors,
                'header_content': header_content,
                'footer_content': footer_content,
                'images': images,
                'class_styles': class_styles
            }
            
            return context
            
        except Exception as e:
            print(f"Error scraping website: {str(e)}")
            return None
    
    async def generate_clone(self, context: dict) -> Optional[str]:
        try:
            # Prepare prompt for Claude
            prompt = f"""You are a web development expert. Your task is to create an HTML clone of the following website.
            Focus on matching the visual design and layout as closely as possible.
            
            Here is the original HTML and design context:
            {context}
            
            Important guidelines:
            1. Pay special attention to background colors of each section and ensure they match the original website exactly.
            2. Preserve the exact structure of headers and footers, including their styling and layout.
            3. Maintain the original CSS classes and their associated styles.
            4. Ensure images are properly positioned and styled.
            5. Match the original website's layout.
            
            Create a complete HTML file with inline CSS that closely matches the original design.
            Include all necessary CSS styles inline to match the original appearance.
            Output ONLY the raw HTML code, nothing else."""
            
            # Call Claude API
            message = self.anthropic.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4000,
                temperature=0.7,
                system="You are a web development expert specializing in creating pixel-perfect HTML clones. Pay special attention to matching headers, footers, and overall structure exactly as they appear in the original website.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return message.content[0].text
            
        except Exception as e:
            print(f"Error generating clone: {str(e)}")
            return None 