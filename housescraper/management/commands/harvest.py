from housescraper.bot.spiders.lianjiahousespider import LianjiaHouseSpider

__author__ = 'awang'

from twisted.internet import reactor

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from housescraper.bot.spiders.housespider import HouseSpider
from housescraper.bot.spiders.anjekehousespider import AnjukeHouseSpider
from housescraper.bot.settings import crawler_setting



from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'run commands to parse feeds'

    def add_arguments(self, parser):
        parser.add_argument(
            '--inc',
            dest='inc',
            help='harvest incrementally'
        )



    def handle(self, *args, **options):
        if options['inc'] == 'ajk' : self.handle_ajk()
        if options['inc'] == 'cap' : self.handle_cap()
        if options['inc'] == 'lj' :  self.handle_lj()


    def handle_cap(self):
        configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
        runner = CrawlerRunner(crawler_setting)
        #d = runner.crawl(AnjukeCaptchaSpider)
        #d.addBoth(lambda _: reactor.stop())
        #reactor.run()
        print 'skip'

    def handle_ajk(self):
        configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
        runner = CrawlerRunner(crawler_setting)
        #d = runner.crawl(HouseSpider)
        d = runner.crawl(AnjukeHouseSpider)
        d.addBoth(lambda _: reactor.stop())
        reactor.run()

    def handle_lj(self):
        configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
        runner = CrawlerRunner(crawler_setting)
        #d = runner.crawl(HouseSpider)
        d = runner.crawl(LianjiaHouseSpider)
        d.addBoth(lambda _: reactor.stop())
        reactor.run()
