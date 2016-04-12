# coding=utf-8
from django.core.exceptions import ObjectDoesNotExist

__author__ = 'awang'
from scrapy import Selector, FormRequest
from housescraper.models import *
from housescraper.bot.items import *
import pdb
import re
import time
import urllib
import requests

from captcha import workdir,run_decaptcha

MS = ":"  # meta separator
MMS = "::"
COMMA = ","

DEFAULT_COMMUNITY_PAGES = 2
DEFAULT_HOUSE_PAGES = 100


class AnjukeCaptchaSpider(scrapy.Spider):
    name = "AnjukeCaptchaSpider"
    def start_requests(self):
        print 'start cap test synced'
        blocked_url = "http://www.anjuke.com/captcha-verify/?callback=shield&history=aHR0cDovL3NoLnp1LmFuanVrZS5jb20vZmFuZ3l1YW4vNjU2NzIwNTI%3D"
        response = self.handle_captcha_response(blocked_url)
        print 'solved captcha',response.url
        return

    def start_requests1(self):
        print 'start cap test'
        blocked_url = "http://www.anjuke.com/captcha-verify/?callback=shield&history=aHR0cDovL3NoLnp1LmFuanVrZS5jb20vZmFuZ3l1YW4vNjU2NzIwNTI%3D"
        request = scrapy.Request(blocked_url, meta={'cookiejar': 1}, callback=self.process_captcha)
        yield  request

    def process_captcha(self, response):
        curl = response.url
        txt = response.body_as_unicode()
        sel = Selector(text=txt)
        captchar_url = sel.xpath('/html/body/div/div[2]/div/div/div/div[2]/div/form/div[1]/img/@src')[0].extract()
        filename = "%s.png"%(time.time())
        r1 = urllib.urlretrieve(captchar_url, workdir+filename)
        captchacookie = ['ajk_boostup_captcha','7c4793e4c72e7bfffbe6b43b9e9cb67a']
        try:
            captchacookie = r1[1]['set-cookie'].split(';')[0].split('=')
        except Exception,e:
            print 'error on captcha cookie, will use default as',e


        result = run_decaptcha(filename)

        error_txt = sel.xpath('/html/body/div/div[2]/div/div/div/div[2]/div/form/div[2]/span')[0].extract()
        print 'current error', error_txt.encode('utf-8')

        request = FormRequest.from_response(
                    response,formnumber=0,
                    #meta={'cookiejar': response.meta['cookiejar']},
                    formdata={
                        'code':result,
                        'submit':'提交'
                    },
                callback=self.process_captcha_result)
        request.cookies[captchacookie[0]] = captchacookie[1]
        #request.headers['Cookie'] = captchacookie[0]+'='+captchacookie[1]

        print request.__dict__
        return [
                request
            ]

    def process_captcha_result(self, response):
        curl = response.url
        txt = response.body_as_unicode()
        sel = Selector(text=txt)
        if curl.find('captcha-verify') != -1:

            error_txt = sel.xpath('/html/body/div/div[2]/div/div/div/div[2]/div/form/div[2]/span')[0].extract()
            print 'captcha recognition failed',response.status
            print 'current error', error_txt.encode('utf-8')

            request = scrapy.Request(curl, callback=self.process_captcha)
            yield  request
        else :
            print "wow passed captcha challenge"

    def handle_captcha_response(self, captcha_url):
        print 'handling captcha page'
        self.crawler.engine.pause()

        times = 0
        while captcha_url.find('captcha-verify') != -1:
            data_post = {
                'code':'',
                'submit':'提交'
            }
            response = requests.post(captcha_url, data=data_post)
            captcha_url = response.url
            times+=1
            print 'trying solving captcha', times,'times'
        self.crawler.engine.start()
        return response


class AnjukeHouseSpider(scrapy.Spider):
    name = "AnjukeHouseSpider"

    def start_requests(self):
        print 'spider start inc mode'
        sources = SourceInfo.objects.filter(name='anjuke')
        self.communities = {} #use name+address to locate
        # pdb.set_trace()

        for source in sources:
            try:
                communities = Community.objects.filter(sid=source.id)
                for community in communities:
                    cmkey = community.name + community.address
                    self.communities[cmkey] = community

                print 'intialized ', len(communities), ' communities'

                print 'spidering data from source %s'%(source.name)
                aurl = source.curl
                aurls = aurl.split(MMS)
                area_strs = aurls[1].split(COMMA)
                type = source.cm_id

                for area_str in area_strs:
                    for page in range(1,200):
                    #settle total pageNumber
                        a1url = aurls[0]%(area_str,page)
                        request = scrapy.Request(a1url, callback=self.parse_house_page)
                        request.meta['s'] = source
                        request.meta['aid'] = area_str
                        request.meta['aurls'] = aurls
                        request.meta['type'] = type
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


    def handle_captcha_response(self, captcha_url):
        print 'handling captcha page'
        #self.crawler.engine.pause()

        times = 0
        while captcha_url.find('captcha-verify') != -1:
            data_post = {
                'code':'',
                'submit':'提交'
            }
            response = requests.post(captcha_url, data=data_post)
            captcha_url = response.url
            times+=1
            print 'trying solving captcha', times,'times'
        #self.crawler.engine.start()
        return response

    def parse_house_page(self, response):
        curl = response.url
        meta = response.meta
        meta['txt'] = response.body_as_unicode()
        if curl.find('captcha-verify') != -1:
            print 'entering captcha page:',curl
            response = self.handle_captcha_response(curl)
            print 'resuming from captcha page'
            meta['txt'] = response.text
            response.meta = meta

        source = response.meta['s']
        aid = response.meta['aid']
        type = response.meta['type']
        txt = meta['txt']
        sel = Selector(text=txt)
        cm_sels = self.extract_field(sel,source,'cm_list')
        print 'parse house list: ', len(cm_sels)

        for cm_sel in cm_sels:
            cm_link = self.extract_field(cm_sel,source,'cm_lastpage')

            request = scrapy.Request(cm_link, callback=self.parse_houses)
            request.meta['s'] = source
            request.meta['type'] = type
            request.meta['aid'] = aid
            request.meta['curls'] = cm_link
            yield request


    def parse_houses(self, response):
        curl = response.url
        meta = response.meta
        meta['txt'] = response.body_as_unicode()
        if curl.find('captcha-verify') != -1:
            print 'entering captcha page:',curl
            response = self.handle_captcha_response(curl)
            print 'resuming from captcha page'
            meta['txt'] = response.text
            response.meta = meta


        source = response.meta['s']
        aid = response.meta['aid']
        type = response.meta['type']

        print 'houses page response',response.url

        txt = meta['txt']
        sel = Selector(text=txt)
        cmfields = ['cm_name','cm_type','cm_addr','cm_cdate','cm_pfee','cm_pcom','cm_ccom',
            'cm_area', 'cm_onrent', 'cm_onsale', 'cm_count', 'cm_parklot', 'cm_greenrate', 'cm_rentrate','cm_holdrate']


        cmdatas = map(lambda x:self.extract_field(sel,source,x), cmfields)
        community = Community(
            id = len(self.communities)+1,
            aid = 0,
            sid = source.id,
            name = cmdatas[0],
            type = cmdatas[1],
            address  = cmdatas[2],
            cdate = cmdatas[3],
            pfee = cmdatas[4],
            pcompany = cmdatas[5],
            ccompany = cmdatas[6],
            area = cmdatas[7],
            onrent = cmdatas[8],
            onsale = cmdatas[9],
            count = cmdatas[10],
            parklot = cmdatas[11],
            greenrate = cmdatas[12],
            rentrate = cmdatas[13],
            holdrate = cmdatas[14]
        )
        cmkey = community.name + community.address
        if not self.communities.has_key(cmkey):
            community.save()
            self.communities[cmkey] = community
            print '+1 community'
        else:
            print 'pick community'
            community = self.communities[cmkey]


        #test if the house row is valid
        hs_name = self.extract_field(sel,source,'hs_name')
        if hs_name == "":
            return
        #collect agent
        agfiels = ['ag_phone','ag_name', 'ag_agency']
        agdata = map(lambda x:self.extract_field(sel,source,x), agfiels)
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
        hsdata = map(lambda x:self.extract_field(sel,source,x), hsfields)
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
