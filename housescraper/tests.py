from django.test import TestCase

# Create your tests here.
from housescraper.models import SourceInfo

s1 = SourceInfo(
    name = "sofang",
    url = "http://sh.sofang.com",
    aurl = "http://sh.sofang.com/home?cityid=332&cityareaid=%d&busid=0&pricetype=&housetype=&keywords=&page=%d::2980,2981",
    curl = "http://sh.sofang.com/community/raa%d-%d.htm::http://sh.sofang.com/community/saa%d-%d.htm",

    cm_list = "XPATH::/html/body/div[4]/table/tr",
    cm_lastpage = "XPATH::/html/body/div[4]/div[2]/ul/li::INDEX::-5::XPATH::a/text()::EXTR::0",
    cm_total = "XPATH::/html/body/div[4]/div[1]/p[2]/span/text()::EXTR::0",

    cm_id = r"XPATH::td[2]/div/p[1]/a/@href::EXTR::0::REG::[r|s]aa(\d+)-\d+.htm",

    cm_name = "XPATH::/html/body/div[4]/div[2]/div[1]/div[1]/div[1]/h2/text()::EXTR::0",
    cm_type = "XPATH::/html/body/div[4]/div[2]/div[1]/div[2]/p[1]/span[1]/text()::EXTR::0",
    cm_addr = "XPATH::/html/body/div[4]/div[2]/div[1]/div[1]/div[1]/p/text()::EXTR::0",
    cm_cdate = "XPATH::/html/body/div[4]/div[2]/div[1]/div[2]/p[2]/span[1]/text()::EXTR::0",
    cm_pfee = "XPATH::/html/body/div[4]/div[2]/div[1]/div[2]/p[2]/span[2]/text()::EXTR::0",
    cm_pcom = "XPATH::/html/body/div[4]/div[2]/div[1]/div[2]/p[3]/text()::EXTR::1",
    cm_ccom = "XPATH::/html/body/div[4]/div[2]/div[1]/div[2]/p[4]/text()::EXTR::1",



    hs_list = "XPATH::/html/body/div[5]/table/tr",
    hs_lastpage = "XPATH::/html/body/div[5]/div[2]/ul/li::INDEX::-5::XPATH::a/text()::EXTR::0",

    ag_phone = "XPATH::td[3]/div/div[2]/p[1]//text()::EXTR::0::REG::(\d+)",
    ag_name = "XPATH::td[3]/div/div[2]/p[1]::EXTR::0::SPLT::0",
    ag_agency = "XPATH::td[3]/div/div[2]/p[2]::EXTR::0",

    hs_name = "XPATH::td[2]/div/p[1]/a/text()::EXTR::0",
    hs_style = "XPATH::td[2]/div/p[3]/text()::EXTR::0",
    hs_deco = "XPATH::td[2]/div/p[3]/text()::EXTR::1",
    hs_dir = "XPATH::td[2]/div/p[3]/text()::EXTR::2",
    hs_stair = "XPATH::td[2]/div/p[3]/text()::EXTR::3",
    hs_update = "XPATH::td[2]/div/p[4]/text()::EXTR::0",
    hs_type = "CONST::0",
    hs_area = "XPATH::td[3]/p/span[1]/text()::EXTR::0",
    hs_cost = "XPATH::td[3]/p/span[3]//text()::JN::0",
    hs_phash = "XPATH::td[1]/div/a/img/@src::EXTR::0"
)