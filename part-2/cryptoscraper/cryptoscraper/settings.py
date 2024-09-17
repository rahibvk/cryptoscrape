# Scrapy settings for cryptoscraper project

BOT_NAME = "cryptoscraper"

SPIDER_MODULES = ["cryptoscraper.spiders"]
NEWSPIDER_MODULE = "cryptoscraper.spiders"

# User-Agent configuration (optional)
USER_AGENT = "cryptoscraper (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS_PER_IP = 8

# Disable cookies
COOKIES_ENABLED = False

# Enable Telnet Console (optional for debugging)
TELNETCONSOLE_ENABLED = True

# Override the default request headers
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en",
}

# Enable or disable spider middlewares
SPIDER_MIDDLEWARES = {
    "scrapy.spidermiddlewares.httperror.HttpErrorMiddleware": 543,
}

# Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware": 543,
    "scrapy.downloadermiddlewares.retry.RetryMiddleware": 550,
}

# Enable or disable extensions
EXTENSIONS = {
    "scrapy.extensions.logstats.LogStats": 500,
}

# Configure item pipelines
ITEM_PIPELINES = {
    "cryptoscraper.pipelines.CryptoscraperPipeline": 300,
}

# Enable and configure the AutoThrottle extension
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = True

# Enable and configure HTTP caching (optional)
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 86400  # Cache for one day
HTTPCACHE_DIR = "httpcache"
HTTPCACHE_IGNORE_HTTP_CODES = [500, 502, 503, 504]
HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# Proxy settings (uncomment and configure if using proxies)
# PROXY_LIST = 'path/to/proxy/list.txt'
# PROXY_MODE = 0
