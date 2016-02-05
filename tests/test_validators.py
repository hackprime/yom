import pytest
from yom.errors import *
from yom.constants import fields
from yom.validators import AppForm, Hash


fully_filled_app = {
    'title': 'fully filled app',
    'description': 'fully filled app',
    'homepage': 'http://google.com',
    'callback': 'http://google.com/callback',
    'scopes': ['fotki:update', 'fotki:delete', 'fotki:write'],
}
less_filled_app_params = {
    'title': 'less filled app',
    'scopes': ['login:email', 'login:avatar'],
}


class FakeArgs(object):
    def __init__(self, defaults=None):
        data = dict.fromkeys(fields)
        if defaults:
            data.update(defaults)
        for key, value in data.items():
            setattr(self, 'input_%s' % key, value)


def test_form_validator():
    with pytest.raises(YomError):
        AppForm()

    validator_from_data = AppForm(data=fully_filled_app)
    validator_from_args = AppForm(args=FakeArgs(fully_filled_app))
    assert validator_from_data.data == validator_from_args.data

    assert validator_from_data.validate() is True
    assert AppForm(data=less_filled_app_params).validate() is True

    data = {'title': 'b', 'homepage': 'c'}
    validator = AppForm(data=data)

    with pytest.raises(YomValidationError):
        validator.validate()
    with pytest.raises(YomValidationError):
        validator.cleaned_data()
    assert validator.is_valid is False

    data = {'title': 'b', 'homepage': None, 'scopes': ['login:avatar']}
    validator = AppForm(data=data)
    is_valid = validator.validate()
    cleaned_data = validator.cleaned_data()
    assert is_valid is True
    assert 'homepage' not in cleaned_data

    with pytest.raises(YomValidationError):
        AppForm(args=FakeArgs()).validate()

    with pytest.raises(YomValidationError):
        AppForm(args=FakeArgs({'title': 'a'})).validate()

    with pytest.raises(YomValidationError):
        AppForm(args=FakeArgs()).validate()

    with pytest.raises(YomValidationError):
        AppForm(new_item=False, args=FakeArgs()).validate()

    with pytest.raises(YomValidationError):
        data = {'title': 'a', 'scopes': ['wrong:scope']}
        AppForm(new_item=False, data=data).validate()


def test_hash_validator():
    app_hash = '70fcd16DD04e4f55b07d30021194b6ac'
    validator = Hash(app_hash)
    data_is_valid = validator.validate()
    assert data_is_valid is True
    assert validator.cleaned_data() == app_hash.lower()

    with pytest.raises(YomValidationError):
        assert Hash(None).validate()

    with pytest.raises(YomValidationError):
        assert Hash('70fcd16').validate()

    with pytest.raises(YomValidationError):
        assert Hash(123).validate()

    with pytest.raises(YomValidationError):
        assert Hash('XYZcd16DD04e4f55b07d30021194b6ac').validate()
