import scrapy
from scrapy_splash import SplashRequest

class CryptospiderSpider(scrapy.Spider):
    name = "cryptospider"
    allowed_domains = ["bscscan.com"]
    start_urls = ["https://bscscan.com/accounts"]

    # Initialize a dictionary to store token counts
    token_counts = {}
    
    # Initialize a set to store already visited wallet URLs
    visited_wallets = set()

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

        # Log the number of links found and current page URL
        self.logger.info(f'Found {len(filtered_links)} address links on page {response.url}')

        # Yield requests to each URL to visit the crypto page
        for url in full_urls:
            # Skip the wallet if it has already been visited
            if url not in self.visited_wallets:
                # Add the wallet to the visited set
                self.visited_wallets.add(url)
                yield SplashRequest(url, self.parse_crypto_page, args={'wait': 2})
            else:
                self.logger.info(f"Skipping already visited wallet: {url}")

        # Handle pagination logic
        if '/accounts' in response.url:
            # Extract current page number, if available
            url_parts = response.url.split('/')
            current_page = url_parts[-1] if url_parts[-1].isdigit() else None
            
            if current_page:
                next_page = int(current_page) + 1
            else:
                next_page = 2  # Start with page 2 if we're on the initial page

            # Ensure next_page does not exceed 400 and there are links to process
            if next_page <= 400 and full_urls:  # Proceed only if there are address links
                next_page_url = f"https://bscscan.com/accounts/{next_page}"
                self.logger.info(f'Requesting next page: {next_page_url}')
                yield SplashRequest(next_page_url, self.parse, args={'wait': 2})

    def parse_crypto_page(self, response):
        # Extract crypto information from each address page
        crypto_items = response.css('.nav-item.list-custom-ERC20')
        wallet_found = False  # Track if any token was found in the wallet

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
                
                # Count the token only if the value is above $1,000
                if value > 1000:
                    wallet_found = True
                    if name in self.token_counts:
                        self.token_counts[name] += 1
                    else:
                        self.token_counts[name] = 1

        # Yield the tokens found in the current wallet (if any)
        if wallet_found:
            yield {'wallet_url': response.url, 'tokens': self.token_counts.copy()}

        # Yield all tokens counts at the end
        if not wallet_found:
            self.logger.info("No tokens found above $1,000 in this wallet.")
