import re

from yom.errors import *
from yom.constants import scopes, fields


class YomValidator(object):
    is_valid = False

    def validate(self):
        is_valid = self._validate()
        self.is_valid = is_valid
        return is_valid

    def cleaned_data(self):
        if not self.is_valid:
            raise YomValidationError('Data is not vaild or not validated yet')
        return self._cleaned_data()


class Hash(YomValidator):
    """
    Application hash validator (128-bit hex number as string)
    """
    def __init__(self, app_hash):
        self.data = app_hash

    def _validate(self):
        if not self.data:
            raise YomValidationError('Hash argument is required')
        if not isinstance(self.data, basestring):
            raise YomValidationError('Hash argument must be a string')
        if re.match(r'[0-9a-f]{32}', self.data, re.I) is None:
            raise YomValidationError('Invalid hash %s' % self.data)
        return True

    def _cleaned_data(self):
        return self.data.lower()


class AppForm(YomValidator):
    """
    Validator of application's creation/edition form.
    """
    def __init__(self, new_item=True, data=None, args=None):
        if not data and not args:
            raise YomError('At least one of data or args should be specified')
        self.data = dict.fromkeys(fields)
        self.data.update(data or self._data_from_args(args))
        self.new_item = new_item

    def _data_from_args(self, args):
        return {name: getattr(args, 'input_%s' % name)
                for name in fields}

    def _validate(self):
        if self.new_item:
            if not self.data['title']:
                raise YomValidationError('Title field is required')
            if not self.data['scopes']:
                raise YomValidationError('Select at least one scope')
        else:
            if not any(self.data[key] for key in fields):
                raise YomValidationError('Supply data to edit')

        if self.data['scopes']:
            undefined_scopes = set(self.data['scopes']) - set(scopes)
            if undefined_scopes:
                raise YomValidationError(
                    'Undefined scopes: %s' % ', '.join(undefined_scopes))
        return True

    def _cleaned_data(self):
        return {key: value for key, value in self.data.items()
                if value is not None}
