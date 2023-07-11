import scrapy
from scrapy_splash import SplashRequest


class CauseiqSpider(scrapy.Spider):
    name = "causeiq"
    allowed_domains = ["www.causeiq.com"]
    #start_urls = ["https://www.causeiq.com/directory/new-jersey-state/"]

    page = 1
    script = '''
        function main(splash, args)
  
        splash.private_mode_enabled = False
        
        headers = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        
        splash:on_request(
            function(request)
            request:set_header('User-Agent', headers)
            end
            )
        
        assert(splash:go(args.url))
        assert(splash:wait(0.5))
        
        splash:set_viewport_full()
        
        assert(splash:wait(5))

        return {
            html = splash:html(),
            --har = splash:har(),
        }
        end
    '''

    def start_requests(self):
        yield SplashRequest(
            url = "https://www.causeiq.com/search/organizations/o_5662f00301503843/?view=list",
            callback= self.parse,
            endpoint="execute",
            args= {
                'lua_source': self.script
            }
            )

    def parse(self, response):
        
        #name, revenue, link = [], [], []

        for item in response.xpath('//div[@class = "search-list-item"]'):

            # name.append(item.xpath('.//h2/a/text()').get())
            # revenue.append(item.xpath('.//div[2]/div[2]/text()').get())
            # link.append(item.xpath('.//h2/a/@href').get())

            yield {
                'Name': item.xpath('.//h2/a/text()').get(),
                'Link': ''.join(['https://www.causeiq.com', item.xpath('.//h2/a/@href').get()]),
                'Location': item.xpath('.//div[1]/div[2]/text()').get(),
                'Industry': item.xpath('.//div[1]/div[1]/text()').get(),
                'Total Revenue': item.xpath('.//div[2]/div[2]/text()').get(),
                'Total Assests': item.xpath('.//div[2]/div[3]/text()').get(),
            }
        

        while self.page < 5063:
            self.page += 1
            next_page = response.urljoin(f"?view=list&page={self.page}")

            print("#########################################################",next_page, "#############################################################")
            yield SplashRequest(url = next_page, callback=self.parse, endpoint='execute',args={'lua_source': self.script})