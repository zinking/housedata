from django.core.exceptions import ObjectDoesNotExist

__author__ = 'awang'
from scrapy import Selector
from housescraper.models import *
from housescraper.bot.items import *
from datetime import datetime
from django.utils import timezone
import pdb
import re
import time

MS = ":"  # meta separator
MMS = "::"
COMMA = ","

DEFAULT_COMMUNITY_PAGES = 2
DEFAULT_HOUSE_PAGES = 100


class HouseSpider(scrapy.Spider):
    name = "HouseSpider"

    def start_requests(self):
        print 'spider start inc mode'
        sources = SourceInfo.objects.all()
        self.hs_raalastpage = {}
        self.hs_saalastpage = {}
        self.cm_lastpage = {}

        for source in sources:
            try:
                print 'spidering data from source %s'%(source.name)
                aurl = source.aurl
                aurls = aurl.split(MMS)
                area_ids = map(lambda x:int(x),aurls[1].split(COMMA))
                if len(area_ids) == 2:
                    area_ids = range(area_ids[0],area_ids[1])

                for area_id in area_ids:
                    #settle total pageNumber
                    a1url = aurls[0]%(area_id,1)
                    request = scrapy.Request(a1url, callback=self.parse_community_first)
                    request.meta['s'] = source
                    request.meta['aid'] = area_id
                    request.meta['aurls'] = aurls
                    yield request

            except Exception,e:
                print e

    def apply_actions(self,sel,actions):
        def apply_action(sel,action):
            (act,val) = action
            if act == 'CSS':
                return sel.css(val)
            elif act == 'XPATH':
                return sel.xpath(val)
            elif act == 'INDEX':
                if len(sel) == 0 :
                    print 'index Nothing', sel
                    return None
                else:
                    id = int(val)
                    return sel[id]
            elif act == 'EXTR':
                if len(sel) == 0 :
                    #print 'Extract Nothing', sel
                    return ""
                else:
                    id = int(val)
                    if id>=len(sel):
                        #print 'EXTRACT ERROR,INDEX OOO',sel,id
                        #print 'EXTRACT ERROR,INDEX OOO',id
                        return ""
                    return sel[id].extract()
            elif act == 'JN':
                if len(sel) == 0:
                    print 'Nothing Join', sel
                else:
                    sels = sel
                    rt = ""
                    for s in sels:
                        rt += s.extract()
                    return rt
            elif act == 'CONST':
                return val
            elif act == 'SPLT':
                sels = sel.split(' ')
                id = int(val)
                return sels[id]
            elif act == 'REG':
                #print 'REG, reg[%s] val[%s]'%(val,sel)
                m = re.search(val,sel)
                if m is None:
                    print 'REG match failed ', val, sel
                    return ""
                else:
                    return m.group(1)
        r = sel
        for action in actions:
            r = apply_action(r,action)
        return r

    def extract_field(self,sel,source,field):
        fd_str = source.__dict__[field]
        fds = fd_str.split(MMS)
        acts = fds[::2]
        vals = fds[1::2]
        actions = zip(acts,vals)
        return self.apply_actions(sel,actions)

    def parse_community_first(self, response):
        source = response.meta['s']
        aid = response.meta['aid']
        aurls = response.meta['aurls']
        txt = response.body_as_unicode()
        sel = Selector(text=txt)

        #correcting the area cm count total page number along the way
        if not self.cm_lastpage.has_key(aid) :
            try:
                cm_lastpage = self.extract_field(sel,source,'cm_lastpage')
                #print 'AREA LAST PAGE', ar_lastpage
                cm_lastpage = int(cm_lastpage)
                self.cm_lastpage[aid] = cm_lastpage
                print aid, 'REPOSITION:Area of communities last page correct to ', cm_lastpage
            except Exception,e:
                #simply skip do nothing
                print 'REPOSITION:error extracting community last page',aid, e

        cm_total = self.extract_field(sel,source,'cm_total')
        print 'IMPORTANT  area %d has %s communities in total: '%(aid,cm_total)

        #requesting all pages
        cpage = 1
        totalpage = DEFAULT_COMMUNITY_PAGES
        if self.cm_lastpage.has_key(aid):
            totalpage = self.cm_lastpage[aid]
            #totalpage = 2

        else:
            print 'WARNING, still didnt get the total page number', aid

        while cpage < totalpage:
            aurl = aurls[0]%(aid,cpage)
            request = scrapy.Request(aurl, callback=self.parse_community)
            request.meta['s'] = source
            request.meta['aid'] = aid
            yield request
            cpage +=1


    def parse_community(self, response):
        source = response.meta['s']
        aid = response.meta['aid']
        txt = response.body_as_unicode()
        sel = Selector(text=txt)
        print 'parse community list ',source.name
        cm_sels = self.extract_field(sel,source,'cm_list')
        print 'parse community list: ', len(cm_sels)

        for cm_sel in cm_sels:
            cm_id = self.extract_field(cm_sel,source,'cm_id')
            if cm_id == "": continue
            cm_id = int(cm_id)
            print 'extracted community id', cm_id
            curls = source.curl.split(MMS)

            #raa
            raaurl1 = curls[0] %(cm_id,1)
            request = scrapy.Request(raaurl1, callback=self.parse_raahouse_first)
            request.meta['s'] = source
            request.meta['cm_id'] = cm_id
            request.meta['type'] = 'rent'
            request.meta['aid'] = aid
            request.meta['curls'] = curls
            print 'request renting community first page', cm_id, raaurl1
            yield request

            #saa
            saaurl1 = curls[1] %(cm_id,1)
            request = scrapy.Request(saaurl1, callback=self.parse_saahouse_first)
            request.meta['s'] = source
            request.meta['cm_id'] = cm_id
            request.meta['type'] = 'sell'
            request.meta['aid'] = aid
            request.meta['curls'] = curls
            print 'request selling community first page', cm_id, saaurl1
            yield request


    def parse_raahouse_first(self, response):
        source = response.meta['s']
        cm_id = response.meta['cm_id']
        aid = response.meta['aid']
        type = response.meta['type']
        curls = response.meta['curls']

        txt = response.body_as_unicode()
        sel = Selector(text=txt)

        hs_total = self.extract_field(sel,source,'hs_total')
        hs_total = int(hs_total)
        print 'IMPORTANT  community %d has %d rent houses in total: '%(cm_id,hs_total)

        if hs_total == 0 :
            print 'SKIP PAGE BECAUSE 0 RECORDS'
            return

        #update last house page along the way
        #correcting the area cm count total page number along the way
        if not self.hs_raalastpage.has_key(cm_id) :
            try:
                hs_lastpage = self.extract_field(sel,source,'hs_lastpage')
                hs_lastpage = int(hs_lastpage)
                self.hs_raalastpage[cm_id] = hs_lastpage
                print 'PageDisvoer: raa cid %d lp %d '%(cm_id,hs_lastpage)
            except Exception,e:
                print 'PageDisvoer: raa cid %d None'%(cm_id)

        curpage = 1
        total_page = DEFAULT_HOUSE_PAGES

        if self.hs_raalastpage.has_key(cm_id):
            total_page = self.hs_raalastpage[cm_id]
        while curpage < total_page:
            ccurl = curls[0] % (cm_id,curpage)
            request = scrapy.Request(ccurl, callback=self.parse_houses)
            request.meta['s'] = source
            request.meta['cm_id'] = cm_id
            request.meta['type'] = type
            request.meta['aid'] = aid
            print 'request renting community', cm_id, ccurl
            yield request
            curpage+=1


    def parse_saahouse_first(self, response):
        source = response.meta['s']
        cm_id = response.meta['cm_id']
        aid = response.meta['aid']
        type = response.meta['type']
        curls = response.meta['curls']

        txt = response.body_as_unicode()
        sel = Selector(text=txt)

        hs_total = self.extract_field(sel,source,'hs_total')
        hs_total = int(hs_total)
        print 'IMPORTANT  community %d has %d sell houses in total: '%(cm_id,hs_total)

        if hs_total == 0 :
            print 'SKIP PAGE BECAUSE 0 RECORDS'
            return

        #update last house page along the way
        #correcting the area cm count total page number along the way
        if not self.hs_saalastpage.has_key(cm_id) :
            try:
                hs_lastpage = self.extract_field(sel,source,'hs_lastpage')
                hs_lastpage = int(hs_lastpage)
                self.hs_saalastpage[cm_id] = hs_lastpage
                print 'PageDisvoer: saa cid %d lp %d '%(cm_id,hs_lastpage)
            except Exception,e:
                print 'PageDisvoer: saa cid %d None'%(cm_id)


        curpage = 1
        total_page = DEFAULT_HOUSE_PAGES

        if self.hs_saalastpage.has_key(cm_id):
            total_page = self.hs_saalastpage[cm_id]
        while curpage < total_page:
            ccurl = curls[0] % (cm_id,curpage)
            request = scrapy.Request(ccurl, callback=self.parse_houses)
            request.meta['s'] = source
            request.meta['cm_id'] = cm_id
            request.meta['type'] = type
            request.meta['aid'] = aid
            print 'request renting community', cm_id, ccurl
            yield request
            curpage+=1

    def parse_houses(self, response):
        source = response.meta['s']
        cm_id = response.meta['cm_id']
        aid = response.meta['aid']
        type = response.meta['type']

        print 'houses page response',response.url

        txt = response.body_as_unicode()
        sel = Selector(text=txt)
        cmfields = ['cm_name','cm_type','cm_addr','cm_cdate','cm_pfee','cm_pcom','cm_ccom']
        cmdatas = map(lambda x:self.extract_field(sel,source,x), cmfields)
        community = Community(
            id = cm_id,
            aid = aid,
            sid = source.id,
            name = cmdatas[0],
            type = cmdatas[1],
            address  = cmdatas[2],
            cdate = cmdatas[3],
            pfee = cmdatas[4],
            pcompany = cmdatas[5],
            ccompany = cmdatas[6]
        )

        community.save()
        print '+1 community'

        hs_sels = self.extract_field(sel,source,'hs_list')


        for hs_sel in hs_sels:
            #test if the house row is valid
            hs_name = self.extract_field(hs_sel,source,'hs_name')
            if hs_name == "":
                continue
            #collect agent
            agfiels = ['ag_phone','ag_name', 'ag_agency']
            agdata = map(lambda x:self.extract_field(hs_sel,source,x), agfiels)
            pn = agdata[0]
            phone_number = 0
            if pn == "":
                phone_number = int(time.time())
            else:
                phone_number = int(agdata[0])
            agent = Agent(
                sid = source.id,
                phone = phone_number,
                name = agdata[1],
                agency = agdata[2]
            )
            agent.save()
            print '+1 agent'

            #collect house
            hsfields = ['hs_name','hs_style','hs_deco', 'hs_dir', 'hs_stair',
                        'hs_update','hs_type', 'hs_area', 'hs_cost', 'hs_phash']
            hsdata = map(lambda x:self.extract_field(hs_sel,source,x), hsfields)
            house_name = hsdata[0]
            if house_name == "":
                print 'Empty house name', response.url, hsdata

            house_cost = hsdata[8]
            if house_cost == None:
                house_cost = ""
                print 'House Cost empty', response.url, hsdata

            house = House(
                sid = source.id,
                cid = community.id,
                aid = agent.phone,
                name = hsdata[0],
                style = hsdata[1],
                deco = hsdata[2],
                dir  = hsdata[3],
                stair = hsdata[4],
                update = hsdata[5],
                type = hsdata[6],
                area = hsdata[7],
                cost = house_cost,
                phash = hsdata[9]
            )
            house.type = type
            house.save()
            print '+1 house'