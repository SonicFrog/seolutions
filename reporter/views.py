from lxml import html
from urllib import parse
from multiprocessing import Pool, Semaphore
import json
import requests
import re

from django.shortcuts import get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpResponseServerError
from google.models import Keyword, Site, Report, KeywordRelation

POOL_SIZE = 5
page_offset = 10
GOOGLE_URI = "https://www.google.fr/search?"


class GoogleCrawler(object):
    name = "Google.fr"

    def crawl(self, storage, site, keywords, semaphore=None, max_page=10):
        uri = GOOGLE_URI + parse.urlencode({'q': keywords})
        good = False

        for x in range(0, max_page):
            current_uri = uri + "&start=" + str(x * page_offset)
            page = requests.get(current_uri)
            tree = html.fromstring(page.text)
            results = tree.xpath('//li[@class="g"]')
            index = 0
            for r in results:
                url = r.xpath("h3/a/@href")
                index = index + 1
                for u in url:
                    clean = re.sub('/url\?q=', "", u)
                    if clean.startswith(site):
                        good = True
                        storage.insert_result(site, x + 1, index, keywords)
        if not good:
            print("Could not find", site, "in the first", max_page, "pages")
            storage.insert_result(site, -1, -1, keywords)
        return good


class DjangoStorage(object):
    def init_storage(self):
        pass

    def insert_result(self, site_url, page, rank, keyword):
        site_obj = get_object_or_404(Site, url=site_url)
        key_obj = get_object_or_404(Keyword, keyword=keyword)
        Report.objects.create(site=site_obj, keyword=key_obj,
                              page=page, rank=rank)


def crawl_google_view(request):
    pool = Pool(POOL_SIZE)
    storage = DjangoStorage()
    crawler = GoogleCrawler()
    sites = get_list_or_404(Site)

    json_data = []

    for site in sites:
        keyword_ids = KeywordRelation.objects.filter(site_id=site.id)
        keywords = Keyword.objects.filter(id__in=keyword_ids)

        json_site = {
            'site': site.name,
            'url': site.url,
            'keywords': [k.keyword for k in keywords],
        }

        json_data.append(json_site)

        for keyword in keywords:
            pool.apply_async(crawler.crawl, (storage, site.url, keyword))

    pool.close()
    pool.join()

    return HttpResponse(json.dumps(json_data))


def crawl_google_view_for_site(request, site_id):
    pass
