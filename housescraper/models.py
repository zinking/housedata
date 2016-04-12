from __future__ import unicode_literals

from django.db import models

# Create your models here.

#house info
#name(title perhaps), community, style, decoration, direction, stairs, last update, area, type, cost

#comminity
#name, types, address, construction_date, property fee, property company, construction company

#agent
#name, phone, agency

class SourceInfo(models.Model):
    name = models.CharField(max_length=1024)
    url = models.TextField()
    aurl = models.TextField() #area url pattern, to gen curl
    curl = models.TextField() #list of community url

    cm_list = models.CharField(max_length=255)
    cm_id = models.CharField(max_length=255)
    cm_lastpage = models.CharField(max_length=255)
    cm_total = models.CharField(max_length=255)


    cm_name = models.CharField(max_length=255)
    cm_type = models.CharField(max_length=255)
    cm_addr = models.CharField(max_length=255)
    cm_cdate = models.CharField(max_length=255)
    cm_pfee = models.CharField(max_length=255)
    cm_pcom = models.CharField(max_length=255)
    cm_ccom = models.CharField(max_length=255)

    cm_area = models.CharField(max_length=255, null=True)
    cm_onrent = models.CharField(max_length=255, null=True)
    cm_onsale = models.CharField(max_length=255, null=True)
    cm_count = models.CharField(max_length=255, null=True)
    cm_parklot = models.CharField(max_length=255, null=True)
    cm_greenrate = models.CharField(max_length=255, null=True)
    cm_rentrate = models.CharField(max_length=255, null=True)
    cm_holdrate = models.CharField(max_length=255, null=True)

    hs_list = models.CharField(max_length=255)
    hs_lastpage = models.CharField(max_length=255)
    hs_total = models.CharField(max_length=255)

    ag_phone = models.CharField(max_length=255)
    ag_name = models.CharField(max_length=255)
    ag_agency = models.CharField(max_length=255)

    hs_name = models.CharField(max_length=255)
    hs_style = models.CharField(max_length=255)
    hs_deco = models.CharField(max_length=255)
    hs_dir = models.CharField(max_length=255)
    hs_stair = models.CharField(max_length=255)
    hs_update = models.CharField(max_length=255)
    hs_type = models.CharField(max_length=255)
    hs_area = models.CharField(max_length=255)
    hs_cost = models.CharField(max_length=255)
    hs_phash = models.CharField(max_length=255)



class Community(models.Model):
    sid = models.BigIntegerField()
    aid = models.BigIntegerField()
    city = models.CharField(max_length=1024)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    type = models.CharField(max_length=1024)
    cdate = models.CharField(max_length=1024)
    pfee = models.CharField(max_length=1024)
    pcompany = models.CharField(max_length=1024)
    ccompany = models.CharField(max_length=1024)

    area = models.CharField(max_length=50, null=True)
    count = models.CharField(max_length=50, null=True)
    onrent = models.CharField(max_length=50, null=True)
    onsale = models.CharField(max_length=50, null=True)
    parklot = models.CharField(max_length=50, null=True)
    greenrate = models.CharField(max_length=50, null=True)
    rentrate = models.CharField(max_length=50, null=True)
    holdrate = models.CharField(max_length=50, null=True) #rongji lv


class Agent(models.Model):
    sid = models.BigIntegerField()
    phone = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=1024)
    agency = models.CharField(max_length=1024)

class House(models.Model):
    sid = models.BigIntegerField()
    cid = models.BigIntegerField()
    aid = models.BigIntegerField()
    name = models.CharField(max_length=1024)
    style = models.CharField(max_length=1024)
    deco = models.CharField(max_length=1024)
    dir  = models.CharField(max_length=1024)
    stair = models.CharField(max_length=1024)
    update = models.CharField(max_length=1024)
    type = models.CharField(max_length=1024) #rent or sell
    area = models.CharField(max_length=1024)
    cost = models.CharField(max_length=1024)
    phash = models.CharField(max_length=1024)
    pdate = models.DateTimeField(auto_now=True,null=True)

"""

class FeedSource(models.Model):
    feed_id     = models.BigIntegerField(db_column='FEED_ID', primary_key=True)  # Field name made lowercase.
    last_etag   = models.CharField()(db_column='LAST_ETAG', max_length=100)  # Field name made lowercase.
    checked     = models.DateTimeField(db_column='CHECKED')  # Field name made lowercase.
    last_url    = models.CharField()(db_column='LAST_URL', max_length=255)  # Field name made lowercase.
    encoding    = models.CharField()(db_column='ENCODING', max_length=15)  # Field name made lowercase.
    xml_url     = models.CharField()(db_column='XML_URL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    title       = models.CharField()(db_column='TITLE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    text        = models.CharField()(db_column='TEXT', max_length=255, blank=True, null=True)  # Field name made lowercase.
    html_url    = models.CharField()(db_column='HTML_URL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    feed_type   = models.CharField()(db_column='FEED_TYPE', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FEED_SOURCE'


class FeedStory(models.Model):
    story_id    = models.BigIntegerField(db_column='STORY_ID', primary_key=True)  # Field name made lowercase.
    feed_id     = models.BigIntegerField(db_column='FEED_ID')  # Field name made lowercase.
    title       = models.CharField()(db_column='TITLE', max_length=255)  # Field name made lowercase.
    link        = models.CharField()(db_column='LINK', max_length=1000)  # Field name made lowercase.
    published   = models.DateTimeField(db_column='PUBLISHED')  # Field name made lowercase.
    updated     = models.DateTimeField(db_column='UPDATED')  # Field name made lowercase.
    author      = models.CharField()(db_column='AUTHOR', max_length=50)  # Field name made lowercase.
    description = models.TextField(db_column='DESCRIPTION')  # Field name made lowercase.
    content     = models.TextField(db_column='CONTENT')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FEED_STORY'


class FeedStructure(models.Model):
    feed_id     = models.BigIntegerField(db_column='FEED_ID', primary_key=True)  # Field name made lowercase.
    start_url   = models.CharField()(db_column='START_URL', max_length=255)  # Field name made lowercase.
    start       = models.CharField()(db_column='START', max_length=1255, blank=True, null=True)  # Field name made lowercase.
    story       = models.CharField()(db_column='STORY', max_length=1255, blank=True, null=True)  # Field name made lowercase.
    title       = models.CharField()(db_column='TITLE', max_length=1255, blank=True, null=True)  # Field name made lowercase.
    link        = models.CharField()(db_column='LINK', max_length=1255, blank=True, null=True)  # Field name made lowercase.
    summary     = models.CharField()(db_column='SUMMARY', max_length=1255, blank=True, null=True)  # Field name made lowercase.
    content     = models.CharField()(db_column='CONTENT', max_length=1255, blank=True, null=True)  # Field name made lowercase.
    author      = models.CharField()(db_column='AUTHOR', max_length=1255, blank=True, null=True)  # Field name made lowercase.
    created     = models.CharField()(db_column='CREATED', max_length=1255, blank=True, null=True)  # Field name made lowercase.
    updated     = models.CharField()(db_column='UPDATED', max_length=1255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FEED_STRUCTURE'

"""