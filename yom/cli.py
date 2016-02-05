import sys
# sys.path.insert(0, '/Users/hackprime/Projects/opensource/yom')
import argparse as a

from grab import Grab
from humanfriendly.tables import format_pretty_table, format_robust_table

from yom import views, conf
from yom.constants import fields, actions
from yom.errors import *
from yom.crawler import authenticate
from yom.validators import AppForm as AppFormValidator, Hash as HashValidator


class Yom(object):
    def __init__(self, args):
        self.args = args

    def _run(self):
        action, data, app_hash, opts = self.prepare_data()

        if action == 'scopes':
            return views.list_scopes()

        view = getattr(views, action)

        kwargs = {}
        if action in ('create', 'edit'):
            validator = AppFormValidator(
                new_item=action == 'create', data=data)
            validator.validate()
            kwargs['data'] = validator.cleaned_data()
        if action in ('edit', 'delete', 'detail'):
            app_hash_validator = HashValidator(app_hash)
            app_hash_validator.validate()
            kwargs['app_hash'] = app_hash_validator.cleaned_data()
        if action == 'delete':
            kwargs['confirm'] = opts['confirm']
        # if action == 'dump':
        #     kwargs['json'] = opts['json']

        kwargs['crawler'] = self.init_crawler()

        prepaired_view = self.prepare_view(view)
        context = prepaired_view(**kwargs)
        return context

    def run(self):
        try:
            result = self._run()
            self.render_output(result)
        except YomContentError as e:
            self.render_message(e)
        except YomError as e:
            self.render_error(e)

    def init_crawler(self):
        crawler = Grab(**conf.YOM_GRAB_CONFIG)
        crawler.go(conf.YOM_INITIAL_URL)
        return crawler

    def prepare_view(self, view):
        return authenticate(view)

    def prepare_data(self):
        action = self.args.action
        data = {name: getattr(self.args, "input_%s" % name) for name in fields}
        app_hash = self.args.app_hash
        opts = {
            'confirm': self.args.opt_confirm,
            # 'json': self.args.opt_json,
        }
        return action, data, app_hash, opts

    def render_output(self, context):
        if 'json' in context:
            print context['json']
        elif 'table' in context:
            print "\n", context['header']
            table_params = {'data': context['table']}
            print format_pretty_table(**table_params), "\n"
        elif 'robust_table' in context:
            print "\n", context['header']
            table_params = {'data': context['robust_table'],
                            'column_names': ['code', '']}
            print format_robust_table(**table_params), "\n"
        elif 'header' in context:
            self.render_message(context['header'])
        else:
            raise YomError('Not enough parameters for output formatting')

    def render_message(self, message):
        print "\n%s\n" % message

    def render_error(self, error):
        print "\n\033[1;31m%s\033[0m\n" % error


def parse_args():
    parser = a.ArgumentParser(prog='yom')

    parser.add_argument(
        'action', choices=actions)
    parser.add_argument(
        'app_hash', nargs='?', help='application hash', default=None)

    # parser.add_argument(
    #     '-f', '--from-file', dest='input_file_path', action='store')
    # parser.add_argument(
    #     '-c', '--clean-cookies', help='Clean auth cookies',
    #     dest='input_clean_cookies', action='store_true')
    parser.add_argument(
        '-y', dest='opt_confirm', action='store_false',
        help='Performing deletion silently, without yes/no dialogue')
    # parser.add_argument(
    #     '--json', dest='opt_json', action='store_false',
    #     help='Dump applications data in JSON')

    parser.add_argument(
        '--title', dest='input_title', action='store')
    parser.add_argument(
        '--description', dest='input_description', action='store')
    parser.add_argument(
        '--homepage', dest='input_homepage', action='store')
    parser.add_argument(
        '--callback', dest='input_callback', action='store')
    parser.add_argument(
        '-s', '--scope', dest='input_scopes', action='append')
    parser.add_argument(
        '-S', '--unscope', dest='input_scopes_uncheck', action='append')

    return parser.parse_args()


def main():
    Yom(parse_args()).run()


if __name__ == '__main__':
    main()
    sys.exit(0)
