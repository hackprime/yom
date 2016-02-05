# YOM - Yandex Oauth application Manager

Console client for [Yandex OAuth service](https://oauth.yandex.com/)

## Why did you do that?

I had a problem: connect complex multi-domain web application project with Yandex authentication service. I prepared all stuff on project's side and faced with final step: register a client application on Yandex. Usually it is not a big deal but there is one annoying detail: you can attach only one absolute callback url to your client application. And when you have about 100 active domains attached to project - the only way is register a bunch of applications, one application per domain, i.e. submit creation form about 100 times **manually**.

So I decided to automate this process using scrapy ([see the gist](https://gist.github.com/hackprime/06573315e0d0a4f7b17e)).

Few weeks later, I totally rewrote it as separate application, just for fun :D

Now it based on [Grab](http://grablib.org/).

**May be unstable, use at your own risc.**

## Installation

Clone a repository on your computer and run:
```
$ python setup.py install
```

## Usage
```
$ yom <command_name> [--param1=value1[ --param2=value2[...]]]
```

## Dependencies

* grab==0.6.30
* humanfriendly==1.43.1

## Docs

Here some command examples. At first run you'll be asked to enter your Yandex login and password. Session cookies will be stored at ``~/.yom.cookies``.

### Retrieving data

#### yom list

Lists brief information about all your applications.

```
$ yom list

Applications list
--------------------------------------------
| 8dbe6e45ee3446d49854cf864e27acde | App 1 |
| ace04056c41f47378d68d54169a19ac2 | App 2 |
--------------------------------------------
```

#### yom detail

Lists detailed information about specified application.

```
$ yom detail 8dbe6e45ee3446d49854cf864e27acde

-------------------------------------------------------------------------------
| title       | App 1                                                         |
| description |                                                               |
| homepage    |                                                               |
| public_key  | 8dbe6e45ee3446d49854cf864e27acde                              |
| secret_key  | 11111111111111111111111111111111                              |
| callback    |                                                               |
| scopes      | ['fotki:update', 'fotki:delete', 'fotki:write', 'fotki:read'] |
-------------------------------------------------------------------------------
```

### Creating/Editing

In commands of this section you need to use following options:

* ``--title`` - title of application
* ``--description`` - short description
* ``--homepage``
* ``--callback`` - callback url
* ``--scope`` (or ``-S``) - right for application (use ``yom scopes`` as reference)

If you passing scope name without colon - all available scopes in selected namespace will be touched. E.g. passing ``--scope fotki`` have the same effect as ``-s fotki:update -s fotki:delete -s fotki:write -s fotki:read``

#### yom create

Creates new application. ``--title`` and at least one ``--scope`` (or shortly ``-s``) are required options.

```
$ yom create --title='App3' --description='Very cool app' --homepage='https://app3.example.com' --callback='http://app3.example.com/callback' -s fotki -s login:email

The "App3" application has been created
-------------------------------------------------------------------------------
| title       | App3                                                          |
| description | Very cool app                                                 |
| homepage    | https://app3.example.com/                                     |
| public_key  | 0848baa9169e4e8ba2a9e3e1417cf3f3                              |
| secret_key  | 22222222222222222222222222222222                              |
| callback    | http://app3.example.com/callback                              |
| scopes      | ['fotki:update', 'fotki:delete', 'fotki:write', 'fotki:read', |
|             |  'login:email']                                               |
-------------------------------------------------------------------------------
```

#### yom edit

Changes any of parameters of an application.
To uncheck scope you can use ``--unscope`` (of ``-S``) option.
Keep in mind that an application must have at least one scope. If your submition won't remain any scope, an error will be raised.

```
$ yom edit 0848baa9169e4e8ba2a9e3e1417cf3f3 --title='App 3 Extended' -S fotki -s postoffice:all

The "App 3 Extended" application has been edited
---------------------------------------------------
| title       | App 3 Extended                    |
| description | Very cool app                     |
| homepage    | https://app3.example.com/         |
| public_key  | 0848baa9169e4e8ba2a9e3e1417cf3f3  |
| secret_key  | 33333333333333333333333333333333  |
| callback    | http://app3.example.com/callback  |
| scopes      | ['login:email', 'postoffice:all'] |
---------------------------------------------------
```

### Deletion

#### yom delete

Deletes specified application. Use ``-y`` option to skip confirmation dialogue.

```
$ yom delete cd6ff8475e674f2ab4c18748d2442bb9
Going to delete application "App3".
Are you sure? [print (Y)es or (N)o]: y

Application "App3" has been deleted
```

## TODO List

* additional commands
    * dump - dump all information about apps, in JSON too.
    * bunch versions for create, edit and delete commands. Main goal - perform action to many applications at one run (input data via file)
    * reset-secret - reset secret key of application
    * uploading icons (maybe)
* clean code
* provide code with comments
* cover code with tests
