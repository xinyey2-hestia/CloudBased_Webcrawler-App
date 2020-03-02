import scrapy
from .author_spider import AuthorSpider
from ..items import BookItem, BookLoader

class BookSpider(scrapy.Spider):
    """Extract information from a /book/show type page on Goodreads"""
    name = "book"
    custom_settings = {
        'CLOSESPIDER_ITEMCOUNT': 200,
        'FEED_URI': 'book.jl',
    }
    def __init__(self,startpage):
        super().__init__()
        self.author_spider = AuthorSpider()
        b = int(startpage)
        self.start_urls = ['https://www.goodreads.com/book/show/{n}'.format(n = n )for n in range(b, 99999)]

    def parse(self, response):
        loader = BookLoader(BookItem(), response=response)

        loader.add_value('url', response.request.url)

        loader.add_css("title", "#bookTitle::text")
        loader.add_value("id", (response.request.url.split('/')[-1]).split('.')[-2])
        loader.add_css('isbn', 'div.infoBoxRowItem>span[itemprop=isbn]::text')
        loader.add_css("author_url", 'meta[property="books:author"]::attr(content)')
        loader.add_css("author", "a.authorName>span::text")
        loader.add_css("num_ratings", "[itemprop=ratingCount]::attr(content)")
        loader.add_css("num_reviews", "[itemprop=reviewCount]::attr(content)")
        loader.add_css("avg_rating", "span[itemprop=ratingValue]::text")
        loader.add_css("image_url", 'meta[property="og:image"]::attr(content)')


        return loader.load_item()

        # author_url = response.css('a.authorName::attr(href)').extract_first()
        # yield response.follow(author_url, callback=self.author_spider.parse)