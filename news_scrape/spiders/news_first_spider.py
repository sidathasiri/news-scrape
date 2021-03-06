import scrapy

class NewsSpider(scrapy.Spider):
    name = "newsfirst"
    start_urls = [
        'https://www.newsfirst.lk/category/local/',
    ]

    def parse(self, response):
        titles = response.css('div.sub-1-news-block::attr(data-page-short-title)').extract()
        dates = response.css('div.sub-1-news-block::attr(data-post-date)').extract()
        for i in range(len(titles)):
            yield {
                'text': titles[i],
                'date': dates[i],
                'source': 'News First',
                'category': 'World'
            }

        # for news in response.css('div.panel-heading'):
        #     yield {
        #         'text': news.css('h3.w-400::text').extract_first()
        #     }
        current_page_number = int(response.css('div.col-xs-12').css('li.active').css('span::text').extract_first())
        if(current_page_number==1):
            next_page = response.url+"page/"+str((current_page_number+1))+"/"
        else:
            next_page = response.url[:-2]+str((current_page_number+1))
        if(current_page_number<40):
            yield scrapy.Request(next_page, callback=self.parse)