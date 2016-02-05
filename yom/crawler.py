from getpass import getpass
from functools import wraps
from string import Formatter

from yom import conf
from yom.errors import *
from yom.constants import scopes as original_scopes


def jump_to(target_url):
    def decorator(func):
        @wraps(func)
        def wrapper(crawler, *args, **kwargs):
            argcount = func.func_code.co_argcount
            argnames = func.func_code.co_varnames[:argcount]
            url_vars = [name for _, name, _, _ in Formatter().parse(target_url)
                        if name is not None]

            if 'app_hash' in url_vars:
                app_hash = args[list(argnames).index('app_hash') - 1] \
                           if args else kwargs.get('app_hash')
                url = target_url.format(app_hash=app_hash)
            else:
                url = target_url

            if url.strip('/') != crawler.doc.url.strip('/'):
                crawler.go(url)

                if crawler.doc.code == 404:
                    raise YomConnectionError('No such resource, '
                                             'check your arguments')
                elif crawler.doc.code \
                        and str(crawler.doc.code).startswith('5'):
                    raise YomConnectionError('Internal server error')

            result = func(crawler, *args, **kwargs)
            return result
        return wrapper
    return decorator


def authenticate(func):
    @wraps(func)
    def wrapper(crawler, *args, **kwargs):
        crawler = authenticate_if_required(crawler)
        # TODO: retry on timeout
        result = func(crawler, *args, **kwargs)
        return result
    return wrapper


def authenticate_if_required(crawler):
    # if crawler.doc.select("//*[not(contains(@class,'passport-header-hidden')) "
    #                       "and contains(@class,"
    #                       "'passport-header-authlink-button')]").exists():
    if 'List of registered clients' not in crawler.doc.body:
        crawler.go(conf.YOM_SIGN_IN_URL)
        crawler.doc.set_input('login', raw_input('Yandex login: '))
        crawler.doc.set_input('passwd', getpass('Yandex password: '))
        crawler.doc.submit()
        # TODO: check whether crawler has logged in or not
    return crawler


def decompress_scopes(scopes):
    decompressed_scopes = []
    for scope in scopes:
        if ':' in scope:
            decompressed_scopes.append(scope)
        else:
            subscopes = [subscope for subscope in original_scopes.keys()
                         if subscope.startswith('%s:' % scope)]
            decompressed_scopes.extend(subscopes)
    return decompressed_scopes


def get_app_hash_from_url(url):
    return url.rsplit('/', 1)[-1]
