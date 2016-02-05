from collections import OrderedDict

actions = ('list', 'detail', 'create', 'edit', 'delete', 'scopes')

fields = ('title', 'description', 'homepage',
          'callback', 'scopes', 'scopes_uncheck')

scopes = OrderedDict([
    ("bsapi", "Banner Storage API"),
    ("bsapi:access", "Access to Banner Storage"),

    ("cloud_api.data", "DataSync API"),
    ("cloud_api.data:user_data", "Access to shared data of users' apps"),
    ("cloud_api.data:app_data", "Storing app data"),

    ("pi", "Yandex Partner Interface"),
    ("pi:all", "Use Yandex API partner interface"),

    ("distribution", "Yandex distribution interface"),
    ("distribution:all", "Using the Yandex distribution API"),

    ("contest", "Yandex.Contest"),
    ("contest:submit", "Sending and testing decisions in competitions"),

    ("direct", "Yandex.Direct"),
    ("direct:api", "Access to Yandex.Direct API"),

    ("cloud_api", "Yandex.Disk REST API"),
    ("cloud_api:disk.app_folder", "Access to app folder in Yandex.Disk"),
    ("cloud_api:disk.info", "Access to information about Yandex.Disk"),
    ("cloud_api:disk.read", "Read all of Yandex.Disk"),
    ("cloud_api:disk.write", "Writing in any place on Yandex.Disk"),

    ("yadisk", "Yandex.Disk WebDAV API"),
    ("yadisk:disk", "Application access to Yandex.Disk"),

    ("display", "Yandex.Display"),
    ("display:all", "Access to banner ad placement"),

    ("lenta", "Yandex.Feeds"),
    ("lenta:all", "Managing Yandex.Subscriptions"),

    ("fotki", "Yandex.Fotki"),
    ("fotki:update", ("Changing data about albums), photos), "
                      "and tags on Yandex.Fotki")),
    ("fotki:delete", "Delete albums), photos and tags on Yandex.Fotki"),
    ("fotki:write", "Upload new albums and photos to Yandex.Fotki"),
    ("fotki:read", ("View public and private albums and photos"
                    "on Yandex.Fotki")),

    ("mail", "Yandex.Mail"),
    ("mail:smtp", "Sending messages via Yandex.Mail on the SMTP protocol"),

    ("pdd", "Yandex.Mail for domains"),
    ("pdd:registrar-auth", ("Reading a list of domains and inboxes), "
                            "connected domains), creating and removing "
                            "inboxes in Yandex.Mail for domain")),

    ("market", "Yandex.Market"),
    ("market:partner-api", "Yandex.Market Partner API"),

    ("metrika", "Yandex.Metrica"),
    ("metrika:write", ("Ability to create counters "
                       "and configure all counter settings")),
    ("metrika:read", ("Access to statistics and "
                      "ability to view all counter settings")),

    ("login", "Yandex.Passport API"),
    ("login:birthday", "Access to date of birth"),
    ("login:email", "Access to email address"),
    ("login:avatar", "Access to user avatar"),
    ("login:info", "Access to username), first name and surname), gender"),

    ("postoffice", "Yandex.Post Office"),
    ("postoffice:all", "Obtaining data"),

    ("yastore", "Yandex.Store"),
    ("yastore:publisher", "Access to Yandex.Store API for Android developers"),

    ("tv", "Yandex.TV"),
    ("tv:use", "Using TV program"),

    ("video", "Yandex.Video"),
    ("video:write", "Create), change), and delete albums and videos"),
    ("video:read", "View albums and videos"),

    ("webmaster", "Yandex.Webmaster"),
    ("webmaster:verify", ("Adding sites to Yandex.Webmaster "
                          "and receiving indexing status information")),
    ("webmaster:hostinfo", ("Obtaining information about external links "
                            "to site")),

    ("appmetrica", "appmetrica"),
    ("appmetrica:write", ("Create apps and change setting parameters "
                          "of both your apps and trusted apps")),
    ("appmetrica:read", ("Obtain statistics and read setting parameters "
                         "of both your apps and trusted apps")),
])

credential_true_names = {'ID': 'public_key', 'Password': 'secret_key',
                         'Callback URL': 'callback'}
