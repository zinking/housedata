__author__ = 'awang'

from twisted.internet import reactor

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from housescraper.bot.spiders.housespider import HouseSpider
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
        if options['inc'] : self.handle_inc()

    def handle_inc(self):
        configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
        runner = CrawlerRunner(crawler_setting)
        d = runner.crawl(HouseSpider)
        d.addBoth(lambda _: reactor.stop())
        reactor.run()
