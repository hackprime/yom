import os

YOM_INITIAL_URL = 'https://oauth.yandex.com'
YOM_DETAIL_URL = 'https://oauth.yandex.com/client/{app_hash}'
YOM_EDIT_URL = 'https://oauth.yandex.com/client/edit/{app_hash}'
YOM_CREATE_URL = 'https://oauth.yandex.com/client/new'
YOM_SIGN_IN_URL = ('https://passport.yandex.com/passport'
                   '?mode=auth&retpath=https://oauth.yandex.ru')

YOM_GRAB_CONFIG = {
    'follow_refresh': True,
    'cookiefile': os.path.join(os.path.expanduser('~'), '.yom.cookies'),
}
