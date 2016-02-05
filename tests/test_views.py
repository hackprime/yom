from copy import deepcopy

from yom import views
from yom.constants import credential_true_names
from yom.crawler import decompress_scopes

from .common import TestGrab

test_data = {
    'title': 'test app',
    'description': 'test desc',
    'homepage': 'https://yandex.ru',
    'callback': 'https://yandex.ru/callback',
    'scopes': ["login:birthday", "login:email",
               "login:avatar", "login:info", 'fotki:delete'],
    'public_key': '00000000000000000000000000000000',
    'secret_key': 'secret_key',
}


def get_common_crawler():
    return TestGrab(data=deepcopy(test_data), select_variants=[
        ("/*[@class='pageTitle']/text()",
         'text', lambda crawler: crawler.data['title']),
        ("*[@class='clientinfo-homepage']/a/@href",
         'text', lambda crawler: crawler.data['homepage']),
        ("//*[contains(@class,'layout-content')]/"
         "*[contains(@class,'clientinfo-description')]",
         'text', lambda crawler: crawler.data['description']),
        ("//*[@class='clientinfo-owner-info']/text()",
         'text_list',
         lambda crawler: ['%s: %s' % (k, crawler.data[v])
                          for k, v in credential_true_names.items()]),
        ("/input[@checked='checked']/@name",
         'text_list', lambda crawler: crawler.data['scopes']),
    ])


def test_get_list_and_list():
    test_titles = ['title1', 'title2', 'title3']
    test_hashes = ['hash1', 'hash2', 'hash3']
    test_urls = ['http://some.url/for/%s' % h for h in test_hashes]

    test_crawler = TestGrab(select_variants=[
        ('/@href', 'text_list', lambda crawler: test_urls),
        ('/text()', 'text_list', lambda crawler: test_titles),
        ("/td/a[@class='clientList-link']", 'exists', lambda crawler: True),
    ])

    expected_data = zip(test_hashes, test_titles)

    view_data = views.get_list(test_crawler)
    assert view_data == expected_data

    context = views.list(test_crawler)
    assert context['table'] == expected_data


def test_get_detail_and_detail():
    test_crawler = get_common_crawler()
    view_data = views.get_detail(test_crawler, test_data['public_key'])
    assert test_data == dict(view_data)

    context = views.detail(test_crawler, test_data['public_key'])
    assert test_data['public_key'] in context['header']
    assert test_data == dict(context['table'])


def test_create():
    test_crawler = get_common_crawler()
    test_data_create = {k: v for k, v in test_data.items()
                        if not k.endswith('_key')}
    context = views.create(test_crawler, test_data_create)

    created_app_data = dict(context['table'])
    assert created_app_data['title'] == test_data_create['title']
    assert created_app_data['public_key'] == test_crawler.data['public_key']
    assert created_app_data['secret_key'] == test_crawler.data['secret_key']
    assert created_app_data['title'] in context['header']


def test_edit():
    test_crawler = get_common_crawler()
    data_to_change = {
        'title': 'new test app title',
        'scopes': ['video', 'tv:use'],
        'scopes_uncheck': ['login:avatar'],
    }
    context = views.edit(test_crawler, data_to_change, test_data['public_key'])

    edited_app_data = dict(context['table'])
    assert edited_app_data['title'] == data_to_change['title']
    assert edited_app_data['secret_key'] == test_crawler.data['secret_key']
    assert edited_app_data['title'] in context['header']

    result_scopes = ((scopes_set(test_data['scopes']) |
                      scopes_set(data_to_change['scopes'])) -
                     scopes_set(data_to_change['scopes_uncheck']))

    assert scopes_set(edited_app_data['scopes']) == result_scopes


def test_delete():
    test_crawler = get_common_crawler()
    context = views.delete(test_crawler, test_data['public_key'])
    assert test_data['title'] in context['header']


def scopes_set(data):
    return set(decompress_scopes(data))
