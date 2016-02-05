from mock import Mock

from yom import conf


class TestGrab(object):
    def __init__(self, data=None, select_variants=None):
        self.data = data
        self.select_variants = select_variants or []

        self.doc = Mock()
        self.doc.select = self.select
        self.doc.submit = self.submit
        self.doc.set_input = self.set_input
        self.doc.form.inputs = FormInputs()
        self.doc.url = conf.YOM_INITIAL_URL

    def select(self, xpath):
        for cond_string, method_name, getter in self.select_variants:
            if cond_string in xpath:
                returned_data = getter(self)
                fake_select = Mock()
                setattr(fake_select, method_name, lambda: returned_data)
                return fake_select
        raise AttributeError('Missed suitable test data for "%s"' % xpath)

    def go(self, url):
        self.doc.url = url

    def submit(self):
        self.go(conf.YOM_DETAIL_URL.format(app_hash=self.data['public_key']))

    def set_input(self, name, value):
        if name.startswith('scopes:'):
            scopes = set(self.data['scopes'])
            scope_name = name.replace('scopes:', '')
            if value is True:
                scopes.add(scope_name)
            elif value is False:
                if scope_name in scopes:
                    scopes.remove(scope_name)
            else:
                raise ValueError(
                    'Ambiguous value for checkbox field: %s' % value)
            self.data['scopes'] = list(scopes)
        else:
            self.data[name] = value


class FormInputs(object):
    def __getitem__(self, key):
        inpt = Mock()
        inpt.checked = True
        return inpt

    def keys(self):
        return ['scopes:1', 'scopes:2']
