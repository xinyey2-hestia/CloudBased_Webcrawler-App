"""Spider to extract information from a /author/show page"""

import scrapy

from ..items import AuthorItem, AuthorLoader

class AuthorSpider(scrapy.Spider):
    name = "author"
    custom_settings = {
        'CLOSESPIDER_ITEMCOUNT': 50,
        'FEED_URI': 'author.jl',
    }
    def __init__(self):
        # The default arg for author_crawl is intentionally a string
        # since command line arguments to scrapy are strings
        super().__init__()


        self.start_urls = ["https://www.goodreads.com/", "https://www.goodreads.com/author/on_goodreads"]

    def parse(self, response):
        url = response.request.url

        # Don't follow blog pages
        if "/blog?page=" in url:
            return

        if url.startswith("https://www.goodreads.com/author/show/"):
            yield self.parse_author(response)



        # If an author crawl is enabled, we crawl similar authors for this author,
        # authors that influenced this author,
        # as well as any URL that looks like an author bio page
        influence_author_urls = response.css('div.dataItem>span>a[href*="/author/show"]::attr(href)').extract()

        for author_url in influence_author_urls:
            yield response.follow(author_url, callback=self.parse)

        similar_authors = response.css('a[href*="/author/similar"]::attr(href)').extract_first()
        if similar_authors:
            yield response.follow(similar_authors, callback=self.parse)

        all_authors_on_this_page = response.css('a[href*="/author/show"]::attr(href)').extract()
        for author_url in all_authors_on_this_page:
            yield response.follow(author_url, callback=self.parse)

    def parse_author(self, response):
        loader = AuthorLoader(AuthorItem(), response=response)
        loader.add_value('url', response.request.url)
        loader.add_css("name", 'h1.authorName>span[itemprop="name"]::text')
        related_authors = response.css('a[href*="/author/similar"]::attr(href)').extract()
        # loader.add_css("genres", 'div.dataItem>a[href*="/genres/"]::text')
        loader.add_value("related_authors", related_authors)

        loader.add_css("avg_rating", 'span.average[itemprop="ratingValue"]::text')
        loader.add_css("num_reviews", 'span[itemprop="reviewCount"]::attr(content)')
        loader.add_css("num_ratings", 'span[itemprop="ratingCount"]::attr(content)')
        loader.add_value("id", (response.request.url.split('/')[-1]).split('.')[-2])
        loader.add_css("image_url", 'meta[itemprop="image"]::attr(content)')

        for row in response.css(".stacked tableList tbody tr"):
            loader.add_value("books", row.xpath("td//text()").extract())




        return loader.load_item()