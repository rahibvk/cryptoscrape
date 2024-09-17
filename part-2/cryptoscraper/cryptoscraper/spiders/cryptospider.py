import scrapy
from scrapy_splash import SplashRequest

class CryptospiderSpider(scrapy.Spider):
    name = "cryptospider"
    allowed_domains = ["bscscan.com"]
    start_urls = ["https://bscscan.com/accounts"]

    def start_requests(self):
        for url in self.start_urls:
            # Send initial request using Splash for JavaScript rendering
            yield SplashRequest(url, self.parse, args={'wait': 2})

    def parse(self, response):
        # Extract links from <a> tags with class 'me-1'
        links = response.css('a.me-1::attr(href)').getall()
        
        # Filter the links to ensure they contain '/address/'
        filtered_links = [link for link in links if '/address/' in link]
        
        # Convert relative links to absolute URLs
        full_urls = [response.urljoin(link) for link in filtered_links]

        # Yield requests to each URL to visit the crypto page
        for url in full_urls:
            yield SplashRequest(url, self.parse_crypto_page, args={'wait': 2})

        # Handle pagination logic
        if '/accounts' in response.url:
            # Extract current page number, if available
            current_page = response.url.split('/')[-1]
            if current_page.isdigit():
                next_page = int(current_page) + 1
            else:
                next_page = 2  # Start with page 2 if we're on the initial page

            # Ensure next_page does not exceed 400 and there are links to process
            if next_page <= 400 and full_urls:  # Proceed only if there are address links
                next_page_url = f"https://bscscan.com/accounts/{next_page}"
                yield SplashRequest(next_page_url, self.parse, args={'wait': 2})

    def parse_crypto_page(self, response):
        # Extract crypto information from each address page
        crypto_items = response.css('.nav-item.list-custom-ERC20')
        for item in crypto_items:
            # Extract crypto name
            name = item.css('.list-name.hash-tag.text-truncate span::attr(data-bs-title)').get()
            
            # Extract crypto value and handle formatting
            value_str = item.css('.text-end .list-usd-value::text').get()
            if value_str:
                try:
                    # Convert the value string into a float, removing commas and dollar signs
                    value = float(value_str.replace(',', '').replace('$', ''))
                except ValueError:
                    continue
                
                # Yield only if the value is above $10,000
                if value > 10000:
                    yield {
                        'name': name,
                        'value': value
                    }
                else:
                    # Since values are in descending order, stop when a value below $10,000 is found
                    break
