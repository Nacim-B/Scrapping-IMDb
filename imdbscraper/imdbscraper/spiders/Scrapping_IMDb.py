import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'top250imdb'
    start_urls = ['https://www.imdb.com/chart/top/?ref_=nv_mv_250']

    def parse(self, response):
        for movies in response.css('td.titleColumn'):
            yield {
                'title': movies.css('a::text').get(),
                'year': movies.css('span.secondaryInfo::text').get().replace('(','').replace(')',''),
                'link': 'https://imdb.com/'+movies.css('a').attrib['href']
            }
    