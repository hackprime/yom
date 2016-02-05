import string
import json as jsonlib
from functools import partial

from grab.spider import Spider, Task

from yom import conf
from yom.errors import YomContentError, YomValidationError
from yom.constants import credential_true_names, scopes
from yom.crawler import (jump_to, authenticate_if_required,
                         decompress_scopes, get_app_hash_from_url)


@jump_to(conf.YOM_CREATE_URL)
def create(crawler, data):
    scopes = data.get('scopes', [])

    for field_name, value in data.items():
        if not field_name.startswith('scopes'):
            crawler.doc.set_input(field_name, value)
    for scope in decompress_scopes(scopes):
        crawler.doc.set_input('scopes:%s' % scope, True)

    crawler.doc.submit()

    app_hash = crawler.doc.url.replace(
        conf.YOM_DETAIL_URL.format(app_hash=''), '')

    app_data = get_detail(crawler, app_hash)
    title = dict(app_data)['title']

    return {
        'header': 'The "%s" application has been created' % title,
        'table': app_data
    }


@jump_to(conf.YOM_EDIT_URL)
def edit(crawler, data, app_hash):
    crawler.go(conf.YOM_EDIT_URL.format(app_hash=app_hash))

    scopes_check = decompress_scopes(data.get('scopes', []))
    scopes_uncheck = decompress_scopes(data.get('scopes_uncheck', []))

    for field_name, value in data.items():
        if not field_name.startswith('scopes'):
            crawler.doc.set_input(field_name, value)

    for scopes, value in ((scopes_check, True), (scopes_uncheck, False)):
        for scope in scopes:
            crawler.doc.set_input('scopes:%s' % scope, value)

    inputs = crawler.doc.form.inputs

    if scopes_uncheck \
            and not any(inputs[name].checked for name in inputs.keys()
                        if name.startswith('scopes')):
        raise YomValidationError('There should remain at least one scope')

    app_hash = crawler.doc.url.replace(
        conf.YOM_EDIT_URL.format(app_hash=''), '')

    crawler.doc.submit()

    app_data = get_detail(crawler, app_hash)
    title = dict(app_data)['title']

    return {
        'header': 'The "%s" application has been edited' % title,
        'table': app_data
    }


@jump_to(conf.YOM_DETAIL_URL)
def delete(crawler, app_hash, confirm=False):
    app_title = get_app_title(crawler)

    if confirm:
        decision = raw_input('Going to delete application "%s".'
                             "\nAre you sure? "
                             '[print (Y)es or (N)o]: ' % app_title)
        if decision.lower() not in ['y', 'yes']:
            return {'header': 'Deletion was canceled'}

    crawler.doc.choose_form_by_element(
        "//form[@class='clientinfo-delete-confirm']")
    crawler.doc.submit()

    return {
        'header': 'Application "%s" has been deleted' % app_title
    }


@jump_to(conf.YOM_INITIAL_URL)
def list(crawler):
    return {
        'header': 'Applications list',
        'table': get_list(crawler)
    }


@jump_to(conf.YOM_DETAIL_URL)
def detail(crawler, app_hash):
    return {
        'header': 'Detailed data for application %s' % app_hash,
        'table': get_detail(crawler, app_hash)
    }


# def dump(crawler, json=False):
#     import logging
#     logging.basicConfig(level=logging.DEBUG)
#     spider = DumpSpider(thread_number=1, priority_mode='const')
#     spider.run()
#     if json:
#         return {
#             'json': jsonlib.dumps(spider.grabbed_items)
#         }
#     else:
#         return {
#             'header': 'All applications',
#             'robust_table': spider.grabbed_items,
#         }


# class DumpSpider(Spider):
#     initial_urls = [conf.YOM_INITIAL_URL]

#     def __init__(self, *args, **kwargs):
#         super(DumpSpider, self).__init__(*args, **kwargs)
#         self._grab_config.update(conf.YOM_GRAB_CONFIG)

#     def set_initial_crawler(self, crawler):
#         self.crawler = crawler

#     def prepare(self):
#         self.grabbed_items = []

#     def task_initial(self, crawler, task):
#         crawler = authenticate_if_required(crawler)
#         uris = get_list(crawler, with_titles=False)

#         print uris
#         for uri in uris:
#             yield Task('detail',
#                        url=conf.YOM_DETAIL_URL.format(app_hash=uri),
#                        meta={'app_hash': uri})
#                        # grab=crawler,
#                        # grab_config=conf.YOM_GRAB_CONFIG,

#     def task_detail(self, crawler, task):
#         self.grabbed_items.append(
#             dict(get_detail(crawler, app_hash=task.meta['app_hash'])))


def list_scopes():
    return {
        'header': 'Available scopes of Yandex OAuth application',
        'robust_table': scopes.items(),
    }


@jump_to(conf.YOM_INITIAL_URL)
def get_list(crawler, with_titles=True):
    item_xpath = (
        "//*[@class='clientList']/*[@class='clientList-row']"
        "/td/a[@class='clientList-link']")

    if not crawler.doc.select(item_xpath).exists():
        raise YomContentError('There are no applications')

    urls = map(get_app_hash_from_url,
               crawler.doc.select('%s/@href' % item_xpath).text_list())
    if with_titles:
        titles = crawler.doc.select('%s/text()' % item_xpath).text_list()
        return zip(urls, titles)
    return urls


@jump_to(conf.YOM_DETAIL_URL)
def get_detail(crawler, app_hash):
    app_params = [
        (
            'title',
            get_app_title(crawler)
        ), (
            'description',
            crawler.doc.select(
                "//*[contains(@class,'layout-content')]/"
                "*[contains(@class,'clientinfo-description')]").text()
        ), (
            'homepage',
            crawler.doc.select("//*[@class='clientinfo-homepage']"
                               "/a/@href").text()
        )
    ]

    credentials = crawler.doc.select(
        "//*[@class='clientinfo-owner-info']/text()").text_list()
    splitted_credentials = map(partial(string.split, sep=':', maxsplit=1),
                               credentials)
    splitted_credentials = [(credential_true_names.get(name, name),
                             value.strip())
                            for name, value in splitted_credentials]
    app_params.extend(splitted_credentials)

    crawler.go(conf.YOM_EDIT_URL.format(app_hash=app_hash))

    scopes = crawler.doc.select(
        "//*[contains(@class, 'js-scopes-permission-checkbox')]"
        "/input[@checked='checked']/@name").text_list()
    scope_name_clean = partial(string.replace,
                               old='scopes:', new='', maxreplace=1)
    app_params.append(('scopes', map(scope_name_clean, scopes)))

    return app_params


def get_app_title(crawler):
    return crawler.doc.select("//*[@class='clientinfo-name']"
                              "/*[@class='pageTitle']/text()").text()
